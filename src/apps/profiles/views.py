from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer


class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer



@api_view(["GET", "POST"])
@permission_classes((permissions.IsAuthenticated,))
def agent_list_api_view(request):
    queryset = Profile.objects.filter(agent=True)
    serializer = ProfileSerializer(queryset, many=True)
    name_spaced_response = {"agents": serializer.data}
    return Response(name_spaced_response, status_code=status.HTTP_200_OK)


class TopAgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True, top_agent=True)
    serializer_class = ProfileSerializer


@api_view(("GET",))
def get_top_agent_list(request):
    agents = Profile.objects.filter(is_agent=True, top_agent=True)
    serializer = ProfileSerializer(agents, many=True)
    name_spaced_response = {"agents": serializer.data}
    return Response(name_spaced_response, status.HTTP_200_OK)


class GetProfileAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [ProfileJSONRenderer]


    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileAPIView(APIView):
    perrmission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def patch(self, request, username):
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)