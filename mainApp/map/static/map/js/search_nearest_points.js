/**
 * This function gets the nearest recycling points from a point
 * @param {double} lat - this is the latitude of a location from which to find nearest point
 * @param {double} long - this is the longitude of a location from which to find nearest point
 * @param {(double)|array} recyclingpoints_list - list of latitude and longitude of recycling points to search from
 * @return {((double|array)|array)} - a list of [latitude, longitude] of the nearest points
 */
function getNearestRecyclingPoints(lat,long,recyclingpoints_list) {

  lookup = sphereKnn(
    /* This array needs to be full of objects that have latitudes and
    * longitudes. Accepted property names are "lat", "latitude", "lon",
    * "lng", "long", "longitude". */
    /* You can also use an array. */
    recyclingpoints_list
  );
  //lookup(latitude,longitude,maxResults,maxDistance)
  var points = lookup(lat, long, 10)
  return points;
}
/**
 * This function processes the output from {@link getNearestRecyclingPoints} to return a dictionary of recycling points.
* @param {list[]} recyclingpoints - list containing the fields of each recycling point as one object
* @return {list[list[],dictionary]} - a list of [list[],dictionary]. The first item is a list [float latitude, float longitude]. The second item is a dictionary with [float latitude, float longitude] as key and an object containing fields for a recycling point as the value. 
*/
function preprocessRecyclingPoints(recyclingpoints) {
  recyclingpoints_lat_long = []
  recyclingpoints_dict = {}
  for(i=0;i<recyclingpoints.length;i++) {
    lat_long = [parseFloat(recyclingpoints[i]["fields"]["latitude"]),parseFloat(recyclingpoints[i]["fields"]["longitude"])]
    recyclingpoints_lat_long.push(lat_long);
    if(recyclingpoints_dict[lat_long]==undefined) {
      recyclingpoints_dict[lat_long]=[recyclingpoints[i]];
    }
    else {
      recyclingpoints_dict[lat_long].push(recyclingpoints[i]);
    }
  }
  return [recyclingpoints_lat_long,recyclingpoints_dict];
}


/**
 * These functions retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
"use strict";
      rad              = Math.PI / 180;
      invEarthDiameter = 1 / 12742018 /* meters */;

/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function sphereKnn(points) {
  /* Inflate the toad! */
  var root = spherekd_build(points)

  /* Lurch off into the sunset! */
  return function(lat, lon, n, max) {
    return spherekd_lookup(lat, lon, root, n, max)
  }
}
      
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function spherical2cartesian(lat, lon) {
  lat *= Math.PI / 180;
  lon *= Math.PI / 180;
  const cos = Math.cos(lat);
  return [cos * Math.cos(lon), Math.sin(lat), cos * Math.sin(lon)]
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
class Position {
  /**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
  constructor(object) {
    let lat = NaN,
        lon = NaN;

    if(Array.isArray(object)) {
      lat = object[0];
      lon = object[1];
    }

    else if(object.hasOwnProperty("location")) {
      lat = object.location[0];
      lon = object.location[1];
    }

    else if(object.hasOwnProperty("position")) {
      lat = object.position[0];
      lon = object.position[1];
    }

    else if(object.hasOwnProperty("geometry") &&
            object.geometry.hasOwnProperty("type") &&
            object.geometry.type === "Point") {
      lat = object.geometry.coordinates[1];
      lon = object.geometry.coordinates[0];
    }

    else {
      if(object.hasOwnProperty("lat")) {
        lat = object.lat;
      }
      else if(object.hasOwnProperty("latitude")) {
        lat = object.latitude;
      }

      if(object.hasOwnProperty("lon")) {
        lon = object.lon;
      }
      else if(object.hasOwnProperty("lng")) {
        lon = object.lng;
      }
      else if(object.hasOwnProperty("long")) {
        lon = object.long;
      }
      else if(object.hasOwnProperty("longitude")) {
        lon = object.longitude;
      }
    }
        /**
     * @type {object}
     */
    this.object   = object;
      /**
     * @type {(double)|array}
     */
    this.position = spherical2cartesian(lat, lon);
  }
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
  static create(object) {
    return new Position(object);
  }
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
  static extract(position) {
    return position.object;
  }
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function spherekd_build(array) {
  return kd_build(array.map(Position.create));
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function spherekd_lookup(lat, lon, node, n, max) {
  return kd_lookup(
      spherical2cartesian(lat, lon),
      node,
      n,
      max > 0 ? 2 * Math.sin(max * invEarthDiameter) : undefined
    ).
    map(Position.extract);
}


/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function Node(axis, split, left, right) {
  this.axis  = axis
  this.split = split
  this.left  = left
  this.right = right
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function distance(a, b) {
  var i = Math.min(a.length, b.length),
      d = 0,
      k

  while(i--) {
    k  = b[i] - a[i]
    d += k * k
  }

  return d
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function byDistance(a, b) {
  return a.dist - b.dist
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function buildrec(array, depth) {
  /* This should only happen if you request a kd-tree with zero elements. */
  if(array.length === 0)
    return null

  /* If there's only one item, then it's a leaf node! */
  if(array.length === 1)
    return array[0]

  /* Uh oh. Well, we have to partition the data set and recurse. Start by
   * finding the bounding box of the given points; whichever side is the
   * longest is the one we'll use for the splitting plane. */
  var axis = depth % array[0].position.length

  /* Sort the points along the splitting plane. */
  /* FIXME: For very large trees, it would be faster to use some sort of median
   * finding and partitioning algorithm. It'd also be a lot more complicated. */
  array.sort(function(a, b) {
    return a.position[axis] - b.position[axis]
  })

  /* Find the median point. It's position is going to be the location of the
   * splitting plane. */
  var i = Math.floor(array.length * 0.5)

  /* Split, recurse, yadda yadda. */
  ++depth

  return new Node(
    axis,
    array[i].position[axis],
    buildrec(array.slice(0, i), depth),
    buildrec(array.slice(i   ), depth)
  )
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function kd_build(array) {
  return buildrec(array, 0)
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function kd_lookup(position, node, n, max) {
  if(!(max > 0))
    max = Number.POSITIVE_INFINITY

  var array = []

  /* Degenerate cases. */
  if(node === null || n <= 0)
    return array

  var stack = [node, 0],
      dist, i

  while(stack.length) {
    dist = stack.pop()
    node = stack.pop()

    /* If this subtree is further away than we care about, then skip it. */
    if(dist > max)
      continue

    /* If we've already found enough locations, and the furthest one is closer
     * than this subtree possibly could be, just skip the subtree. */
    if(array.length === n && array[array.length - 1].dist < dist * dist)
      continue

    /* Iterate all the way down the tree, adding nodes that we need to remember
     * to visit later onto the stack. */
    while(node instanceof Node) {
      if(position[node.axis] < node.split) {
        stack.push(node.right, node.split - position[node.axis])
        node = node.left
      }

      else {
        stack.push(node.left, position[node.axis] - node.split)
        node = node.right
      }
    }

    /* Once we've hit a leaf node, insert it into the array of candidates,
     * making sure to keep the array in sorted order. */
    dist = distance(position, node.position)
    if(dist <= max * max)
      binary_insert({object: node, dist: dist}, array, byDistance)

    /* If the array's too long, cull it. */
    if(array.length > n)
      array.pop()
  }

  /* Strip candidate wrapper objects. */
  i = array.length

  while(i--)
    array[i] = array[i].object

  return array
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function defaultComparator(a, b) {
  return a - b
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function binary_search (item, array, comparator) {
  if(!comparator)
    comparator = defaultComparator

  var low  = 0,
      high = array.length - 1,
      mid, comp

  while(low <= high) {
    mid  = (low + high) >>> 1
    comp = comparator(array[mid], item)

    if(comp < 0)
      low = mid + 1

    else if(comp > 0)
      high = mid - 1

    else
      return mid
  }

  return -(low + 1)
}
/**
 * function retrieved from @see https://github.com/darkskyapp/sphere-knn
*/
function binary_insert(item, array, comparator) {
  var i = binary_search(item, array, comparator)

  if(i < 0)
    i = -(i + 1)

  array.splice(i, 0, item)
}