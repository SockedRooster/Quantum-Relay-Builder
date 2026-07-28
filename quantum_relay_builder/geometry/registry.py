from collections import defaultdict


class PartRegistry:
    """Tracks generated objects by semantic category and unique object name."""

    def __init__(self):
        self._categories = defaultdict(list)
        self._by_name = {}

    def add(self, category, obj):
        if obj.name in self._by_name:
            raise ValueError(f"Duplicate generated object name: {obj.name}")

        self._categories[category].append(obj)
        self._by_name[obj.name] = obj
        return obj

    def extend(self, category, objects):
        for obj in objects:
            self.add(category, obj)
        return objects

    def get(self, category):
        return tuple(self._categories.get(category, ()))

    def find(self, object_name):
        return self._by_name.get(object_name)

    def counts(self):
        return {
            category: len(objects)
            for category, objects in self._categories.items()
        }

    def categories(self):
        return tuple(sorted(self._categories.keys()))

    def all_objects(self):
        return tuple(self._by_name.values())
