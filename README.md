# TraversalMaykr-Py-GUI
A Python GUI tool to generate `idInfoTraversal` and `idInfo_TraversalChain` (+ `idInfo_TraversalPoint`) entities for Doom Eternal. Based on Powerball253's [TraversalMaykr](https://github.com/PowerBall253/TraversalMaykr).

## Usage
### General
I wrote this script based coordinates being gathered using `where`, and then pasting it into the coordinates field. You can still manually enter them, in the format `x y z`, ex. `12 34 56` or `13.12 509.2 87.1123`.

The starting entity number is the number appended to the name of the generated entity. For example, if you set it to 24 and made a traversal info for soldiers, then the generated entity would be named `mod_info_traversal_soldier_00024`. This number automatically increments by 1 after every generated entity.

The boxes checked under "Monster Type Selection" control what demons the traversal entities are generated for. You can also select one of the presets below instead.

"Clear Coordinates (and Midpoints)" clears all the input fields on the left side of the interface, including any stored values like midpoints.

"Clear Output File" clears the contents of the txt that the generated entities are written to.

### Traversal Info
Creates `idInfoTraversal` entities.
1. Enter the coordinates for the start point of the traversal in "Start Coordinates"
2. Use the "Animation to Destination" dropdown menu to pick the animation you want the demon to use to get from the start point to the end point
3. Enter the coordinates for the end point of the traversal in "Destination Coordinates"
4. Set an starting number for the entity, and select the monster types you want
5. Select "Create Reciprocal Traversal" if you want
    * It will make another set of traversals, using the start coords as the destinations & vice versa, and also reversing the given animation. The reciprocal entity will have `_r` appended to its name
6. Then click "Generate Traversals"
    * This won't clear any of the input fields on the left

### Traversal Chain
Creates `idInfo_TraversalChain` and `idInfo_TraversalPoint` entities.
1. Enter the coordinates for the start point of the traversal chain in "Start Coordinates"
2. Use the "Animation to First Midpoint" dropdown menu to pick the animation you want the demon to use to get from the start point to the first midpoint
3. Enter the coordinates for a midpoint of the traversal chain in "Midpoint Coordinates"
4. Use the "Animation to Next Midpoint/Destination" dropdown menu to pick the animation you want the demon to use to get to the next midpoint or destination
5. Click "Add Midpoint" and the coords and animation you entered will show in the list below
6. Repeat steps 3-5 if you want to add more midpoints
7. Enter the coordinates for the end point of the traversal chain in "Destination Coordinates"
8. Set an starting number for the entity, and select the monster types you want
9. Select "Create Reciprocal Traversal Chain" if you want
    * It will make another set of traversal chains, using the start coords as the destinations & vice versa, reversing the order of midpoints, and also reversing the given animations. The reciprocal entity will have `_r` appended to its name
9. Then click "Generate Traversal Chains"
    * Clicking this will clear all of the input fields on the left
	
## Misc. Notes/Known Issues
* Clicking "Generate Traversal" with some empty fields causes the program to crash.
* Wolf traversals don't work properly outside of ledge up/down & jump forward animations, since it has such a limited pool of animations. I'm still working on a way around that.
* The `[Settings]` section in `config.ini` is mainly for console input/output, which I use for testing before setting up the GUI. These settings should be left as is when using the GUI.
