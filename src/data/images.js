// Centralized image URLs (Unsplash, nature/sustainability themed).
// Swap these for your own brand assets when adapting the template.
const img = (id, w = 1200) =>
  `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=${w}&q=80`

export const images = {
  heroRoad: img('1448375240586-882707db888b', 1600), // aerial road through forest
  grass: img('1500382017468-9049fed747ef'), // grass field
  mountain: img('1464822759023-fed622ff2c3b'), // mountain peaks
  forest: img('1441974231531-c6227db76b6e', 1400), // forest trees
  plant1: img('1466692476868-aef1dfb1e735'), // plant leaves
  plant2: img('1518531933037-91b2f5f229cc'), // green plant
  lake: img('1506905925346-21bda4d32df4', 1600), // mountain lake aerial
  roadAerial: img('1470770841072-f978cf4d019e', 1600), // winding road aerial
  avatar1: img('1438761681033-6461ffad8d80', 200),
  avatar2: img('1500648767791-00dcc994a43e', 200),
  avatar3: img('1494790108377-be9c29b29330', 200),
}
