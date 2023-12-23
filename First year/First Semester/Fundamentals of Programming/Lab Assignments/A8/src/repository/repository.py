from src.repository.repositoryException import RepositoryException


class Repository:
    def __init__(self):
        self._data = {}

    def add(self, object_entity):
        if object_entity.id in self._data:
            raise RepositoryException("Instance with this ID: " + str(object_entity.id) + " already exists")
        self._data[object_entity.id] = object_entity

    def remove(self, object_id):
        object_id = int(object_id)
        if object_id not in self._data:
            raise RepositoryException("Instance with this ID: " + str(object_id) + " does not exist")
        del self._data[object_id]

    def update(self, object_entity):
        self._data[int(object_entity.id)] = object_entity

    def get_all(self):
        return list(self._data.values())

    def get_data_dictionary(self):
        return self._data

    def search_by_id(self, object_id):
        object_id = int(object_id)

        list_of_instances = []

        _id = str(object_id)

        for object_instance in self._data.values():
            object_instance_id = str(object_instance.id)
            if _id in object_instance_id:
                list_of_instances.append(object_instance)

        return list_of_instances

    def search_by_name(self, object_name):
        list_of_instances = []

        _name = object_name.lower()

        for object_instance in self._data.values():
            object_instance_name = object_instance.name.lower()
            if _name in object_instance_name:
                list_of_instances.append(object_instance)

        return list_of_instances

    def search_by_title(self, object_title):
        list_of_instances = []

        _title = object_title.lower()

        for object_instance in self._data.values():
            object_instance_title = object_instance.title.lower()
            if _title in object_instance_title:
                list_of_instances.append(object_instance)

        return list_of_instances

    def search_by_description(self, object_description):
        list_of_instances = []

        _description = object_description.lower()

        for object_instance in self._data.values():
            object_instance_description = object_instance.description.lower()
            if _description in object_instance_description:
                list_of_instances.append(object_instance)

        return list_of_instances

    def search_by_genre(self, object_genre):
        list_of_instances = []

        _genre = object_genre.lower()

        for object_instance in self._data.values():
            object_instance_genre = object_instance.genre.lower()
            if _genre in object_instance_genre:
                list_of_instances.append(object_instance)

        return list_of_instances
