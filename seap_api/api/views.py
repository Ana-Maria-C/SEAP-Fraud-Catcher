from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.acquisition_service import AcquisitionService
from .serializers import AcquisitionSerializer
from .serializers import ItemSerializer
from .services.item_service import ItemService


class AcquisitionListView(APIView):
    def get(self, request):
        """
        Retrieves the last 10 acquisitions for display purposes.
        """
        acquisitions = AcquisitionService.get_all_acquisitions()
        acquisitions = acquisitions[:10]  # Retrieve the last 10 acquisitions
        serializer = AcquisitionSerializer(acquisitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new acquisition along with associated items.
        """
        try:
            acquisition_data = request.data.get("acquisition")
            items_data = request.data.get("items", [])
            acquisition = AcquisitionService.create_acquisition_with_items(acquisition_data, items_data)
            serializer = AcquisitionSerializer(acquisition)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AcquisitionDetailView(APIView):
    def get(self, request, acquisition_id):
        """
        Retrieve a single acquisition and its associated items by acquisition_id.
        """
        try:
            print(f"Fetching acquisition_id: {acquisition_id}")  # Debug log
            acquisition = AcquisitionService.get_acquisition_with_items(acquisition_id)
            print(f"Acquisition: {acquisition}")  # Debug log
            if acquisition:
                return Response(acquisition, status=status.HTTP_200_OK)
            return Response({"error": "Acquisition not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error fetching acquisition: {str(e)}")  # Debug log
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, acquisition_id):
        """
        Update an acquisition by acquisition_id.
        """
        try:
            update_data = request.data
            acquisition = AcquisitionService.update_acquisition(acquisition_id, update_data)
            serializer = AcquisitionSerializer(acquisition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, acquisition_id):
        """
        Delete an acquisition by acquisition_id.
        """
        try:
            success = AcquisitionService.delete_acquisition(acquisition_id)
            if success:
                return Response({"message": "Acquisition deleted successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Acquisition not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemsListView(APIView):
    def get(self, request):
        """
        Retrieves the last 10 items for display purposes.
        """
        items = ItemService.get_all_items()
        items = items[:10]  # Retrieve the last 10 items
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new acquisition along with associated items.
        """
        try:
            item_data = request.data
            item = ItemService.create_item(item_data)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(APIView):
    def get(self, request, acquisition_id):
        """
        Retrieve a single item by acquisition_id.
        """
        try:
            print(f"Fetching item_id: {acquisition_id}")  # Debug log
            item = ItemService.get_items_by_acquisition(acquisition_id)
            print(f"Item: {item}")  # Debug log
            if item:
                return Response(item, status=status.HTTP_200_OK)
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error fetching item: {str(e)}")  # Debug log
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, item_id):
        """
        Update an item by item_id.
        """
        try:
            update_data = request.data
            item = ItemService.update_item(item_id, update_data)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, item_id):
        """
        Delete an item by item_id.
        """
        try:
            success = ItemService.delete_item(item_id)
            if success:
                return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
