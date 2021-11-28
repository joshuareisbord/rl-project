


def sort_coordinates(coordinates, starting_point):
    distances = []
    for position in coordinates:
        distance = manhattan_distance(starting_point, position)
        distances.append(distance)
    sorted_distances, sorted_coordinates = two_way_merge_sort(distances, coordinates)
    return sorted_distances, sorted_coordinates
    
def manhattan_distance(start, end):
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return distance

## Helper functions
def two_way_merge_sort(distances, coordinates):
    """
    Purpose:
        Sorts distances in ascending order. Applies same sorting updates to coordinates to maintain index relationship.
    Args:
        distances - list of distances.
        coordinates - list of coordinates.
    Returns:
        Sorted distances in ascending order and related coordinates.
    """
    number_of_distances = len(distances)
    if number_of_distances == 1 or number_of_distances == 0: return distances, coordinates
    # Gets mid point in list. Coordinates length equals distances length so mid value is the same.
    mid = number_of_distances // 2

    # Gets lists to the left of the mid point.
    left_distances = distances[:mid]
    left_coordinates = coordinates[:mid]
    # Gets lists to the right of the mid point.
    right_distances = distances[mid:]
    right_coordinates = coordinates[mid:]

    # Split left side.
    left_distances, left_coordinates = two_way_merge_sort(left_distances, left_coordinates)
    # Split right side.
    right_distances, right_coordinates = two_way_merge_sort(right_distances, right_coordinates)
    # Combine and sort both sides.
    return two_way_merge(left_distances, right_distances, left_coordinates, right_coordinates)

def two_way_merge(left_distances, right_distances, left_coordinates, right_coordinates):
    """
    Purpose:
        Performs the merge sort.
    Args:
        left_distances - List of distances left of mid point.
        right_distances - List of distances right of mid point.
        left_coordinates - List of coordinates left of mid point.
        right_coordinates - List of coordinates right of mid point.
    Returns:
        sorted_distances - List of distances sorted in ascending order.
        sorted_coordinates - List of coordinates sorted based on distance in ascending order.
    """
    sorted_distances = []
    sorted_coordinates = []

    # Performs sort until either side is empty.
    while left_distances != [] and right_distances != []:
        # Compares values, adds the greater value to sorted arrays, remove element from arrays to be evaluated.
        if left_distances[0] < right_distances[0]:
            sorted_distances.append(left_distances[0])
            left_distances.pop(0)
            sorted_coordinates.append(left_coordinates[0])
            left_coordinates.pop(0)
        else:
            sorted_distances.append(right_distances[0])
            right_distances.pop(0)
            sorted_coordinates.append(right_coordinates[0])
            right_coordinates.pop(0)
            
    # Adds remaining values to sorted arrays.
    while left_distances != []:
        sorted_distances.append(left_distances[0])
        left_distances.pop(0)
        sorted_coordinates.append(left_coordinates[0])
        left_coordinates.pop(0)
    # Adds remaining values to sorted arrays.
    while right_distances != []:
        sorted_distances.append(right_distances[0])
        right_distances.pop(0)
        sorted_coordinates.append(right_coordinates[0])
        right_coordinates.pop(0)
    
    return sorted_distances, sorted_coordinates