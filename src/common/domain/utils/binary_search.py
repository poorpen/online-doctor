from typing import List, Any, Callable


def binary_search(collection: List[Any], search_object: Any, value_getter: Callable) -> Any:
    left = 0
    right = len(collection) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_item = collection[mid]
        if value_getter(mid_item) == search_object:
            return mid_item
        elif value_getter(mid_item) < search_object:
            left = mid + 1
        elif value_getter(mid_item) > search_object:
            right = mid - 1
