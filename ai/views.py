from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
import numpy  as np

from .models import KnowledgeEmbedding
from .services import get_ai_provider
from usage.models import UsageLog
from workspaces.models import Workspaces, Membership


def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    denom = (np.linalg.norm(v1) * np.linalg.norm(v2))
    if denom == 0:
        return 0.0
    return float(np.dot(v1, v2) / denom)


def user_can_access_workspace(user, workspace) -> bool:
    """Check if user is owner or has membership in workspace."""
    if not user.is_authenticated:
        return False
    if workspace.owner_id == user.id:
        return True
    return Membership.objects.filter(workspace=workspace, user=user).exists()


class WorkspaceAIQueryView(APIView):
    def post(self, request, workspace_id):
        question = request.data.get("question")
        if not question:
            return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure workspace exists
        workspace = get_object_or_404(Workspaces, id=workspace_id)

        # Permission check
        if not user_can_access_workspace(request.user, workspace):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        provider = get_ai_provider()

        # Step 1: Generate embedding for the question
        try:
            question_embedding = provider.generate_embedding(question)
        except Exception as e:
            return Response({"error": f"Failed to generate embedding: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 2: Fetch all embeddings for this workspace
        embeddings_qs = KnowledgeEmbedding.objects.filter(workspace_id=workspace_id).only("id", "content", "embedding")
        if not embeddings_qs.exists():
            return Response({"error": "No embeddings found for this workspace"}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Compute similarity scores
        scored = []
        for e in embeddings_qs:
            try:
                score = cosine_similarity(question_embedding, e.embedding)
                scored.append((score, e))
            except Exception:
                continue

        if not scored:
            return Response({"error": "No valid embeddings to compare"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Step 4: Sort by similarity and take top N
        TOP_N = 5
        top_embeddings = [e for _, e in sorted(scored, key=lambda x: x[0], reverse=True)[:TOP_N]]

        # Step 5: Build context
        context = " ".join(e.content for e in top_embeddings)

        # Step 6: Generate answer
        try:
            answer = provider.generate_answer(question, context)
        except Exception as e:
            UsageLog.objects.create(
                user=request.user,
                workspace_id=workspace_id,
                action="ai_query_failed",
                metadata={"error": str(e), "provider": "deepseek", "context_size": len(top_embeddings)}
            )
            return Response({"error": "AI provider failed"}, status=status.HTTP_502_BAD_GATEWAY)

        # Step 7: Log usage
        UsageLog.objects.create(
            user=request.user,
            workspace_id=workspace_id,
            action="ai_query",
            metadata={
                "provider": "deepseek",
                "context_size": len(top_embeddings),
                "question_length": len(question),
                "timestamp": timezone.now().isoformat()
            }
        )

        return Response({"question": question, "answer": answer})
