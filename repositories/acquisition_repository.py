from models.acquisition import Acquisition
from models.item import Item


class AcquisitionRepository:
    """
    A repository class that handles all database operations related to the Acquisition model.
    """

    @staticmethod
    def get_acquisition_with_items(acquisition_id: str):
        """
        Retrieves an acquisition and its associated items using MongoDB aggregation pipeline.

        Parameters:
        -----------
        acquisition_id : str
            The acquisition ID to retrieve.

        Returns:
        --------
        dict
            A dictionary representing the acquisition with its associated items.
        """
        pipeline = [
            {"$match": {"acquisition_id": acquisition_id}},
            {
                "$lookup": {
                    "from": "items",  # The collection we're joining with
                    "localField": "_id",  # The field in the Acquisition document
                    "foreignField": "acquisition",  # The field in the Items document (reference to Acquisition)
                    "as": "items",  # Name of the field that will contain the joined documents
                }
            },
        ]

        # Execute the aggregation pipeline
        result = list(Acquisition.objects.aggregate(pipeline))

        # Return the first acquisition with its items, or None if no result
        return result[0] if result else None

    @staticmethod
    def insert_acquisition(acquisition_data):
        """
        Inserts a new acquisition into the database.

        Parameters:
        -----------
        acquisition_data : dict
            A dictionary containing the acquisition data to insert.

        Returns:
        --------
        Acquisition
            The saved Acquisition object.
        """
        acquisition = Acquisition(**acquisition_data)
        acquisition.save()
        return acquisition

    @staticmethod
    def update_acquisition(acquisition_id, update_data):
        """
        Updates an existing acquisition.

        Parameters:
        -----------
        acquisition_id : str
            The ID of the acquisition to update.
        update_data : dict
            A dictionary containing the updated fields for the acquisition.

        Returns:
        --------
        Acquisition
            The updated Acquisition object.
        """
        acquisition = Acquisition.objects(acquisition_id=acquisition_id).first()
        if acquisition:
            acquisition.update(**update_data)
            acquisition.reload()  # Reload to get the updated document
        return acquisition

    @staticmethod
    def delete_acquisition(acquisition_id):
        """
        Deletes an acquisition by its ID.

        Parameters:
        -----------
        acquisition_id : str
            The ID of the acquisition to delete.

        Returns:
        --------
        bool
            True if the deletion was successful, False if not found.
        """
        acquisition = Acquisition.objects(acquisition_id=acquisition_id).first()
        if acquisition:
            acquisition.delete()
            return True
        return False

    @staticmethod
    def get_all_acquisitions():
        """
        Retrieves all acquisitions from the database.

        Returns:
        --------
        list
            A list of Acquisition objects.
        """
        return Acquisition.objects.all()

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
        return Acquisition.objects(cpv_code_id=cpv_code_id)
