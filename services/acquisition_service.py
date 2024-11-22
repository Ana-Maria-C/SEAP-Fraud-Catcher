from repositories.acquisition_repository import AcquisitionRepository
from repositories.item_repository import ItemRepository
from seap_api.api.utils.filter_utils import filter_acquisition_data, filter_item_data


class AcquisitionService:
    """
    A service class that handles business logic for acquisitions.
    """

    @staticmethod
    def create_acquisition_with_items(acquisition_data, items_data):
        """
        Creates a new acquisition and associates multiple items with it.

        Parameters:
        -----------
        acquisition_data : dict
            Data for creating the acquisition.
        items_data : list of dict
            List of item data dictionaries to associate with the acquisition.

        Returns:
        --------
        Acquisition
            The created acquisition object.
        """
        filtered_acquisition_data = filter_acquisition_data(acquisition_data)
        if not filtered_acquisition_data.get("acquisition_id"):
            raise ValueError(
                "acquisition_id is None or missing in the acquisition data"
            )

        acquisition = AcquisitionRepository.insert_acquisition(
            filtered_acquisition_data
        )

        for item_data in items_data:
            filtered_item_data = filter_item_data(item_data)
            filtered_item_data["acquisition"] = acquisition
            ItemRepository.insert_item(filtered_item_data)

        return acquisition

    @staticmethod
    def get_acquisition_with_items(acquisition_id):
        """
        Retrieves an acquisition along with its associated items using an aggregation pipeline.

        Parameters:
        -----------
        acquisition_id : str
            The ID of the acquisition to retrieve.

        Returns:
        --------
        dict
            The acquisition and its items.
        """
        return AcquisitionRepository.get_acquisition_with_items(acquisition_id)

    @staticmethod
    def update_acquisition(acquisition_id, update_data):
        """
        Updates an acquisition by its ID.

        Parameters:
        -----------
        acquisition_id : str
            The ID of the acquisition to update.
        update_data : dict
            A dictionary containing the updated fields.

        Returns:
        --------
        Acquisition
            The updated acquisition object.
        """
        filtered_update_data = filter_acquisition_data(update_data)
        return AcquisitionRepository.update_acquisition(
            acquisition_id, filtered_update_data
        )

    @staticmethod
    def delete_acquisition(acquisition_id):
        """
        Deletes an acquisition and cascades the deletion to all associated items.

        Parameters:
        -----------
        acquisition_id : str
            The ID of the acquisition to delete.

        Returns:
        --------
        bool
            True if the acquisition and its items were successfully deleted, False otherwise.
        """
        # Delete acquisition and all related items
        items = ItemRepository.get_items_by_acquisition(acquisition_id)
        for item in items:
            ItemRepository.delete_item(item.id)

        return AcquisitionRepository.delete_acquisition(acquisition_id)

    @staticmethod
    def get_all_acquisitions():
        """
        Retrieves all acquisitions from the database.

        Returns:
        --------
        list
            A list of all acquisitions.
        """
        return AcquisitionRepository.get_all_acquisitions()

    @staticmethod
    def get_acquisitions_by_cpv_code_id(cpv_code_id):
        """
        Retrieves all acquisitions with the specified CPV code ID.

        Parameters:
        -----------
        cpv_code_id : int
            The CPV code ID to filter acquisitions.

        Returns:
        --------
        list
            A list of Acquisition objects that match the given CPV code ID.
        """
        return AcquisitionRepository.get_acquisitions_by_cpv_code_id(cpv_code_id)
