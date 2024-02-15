# pseudo code how to rewrite the move function


GetMoveToThings(....)
Keep going in player direction
If position is 
- on ground map and not -1
- object
- oversized object
- invisible object
- tile
Then
Add to array moveToArr
Ordered by closest to player 


On move:
moveToArr = getMoveToThings(player direction = x or -x or y or -y, player position)

For each moveToArr

If (check all the things that can combine for i and i+1
Combine i and i+1
If can't
Try i+1 and i+2 and wo on until end of arr

If one combined, stop and
Then check if any oversized object is complete and disappear it
Then
move player and everything between that place and player in the direction
Then
Check player and tile


Check all the things that can combine zacne s hracem a co je u nej a pak ta priorita veci co jsi psal


Kdyz se nic nezkombinuje tak
- je na konci prazdny misto,
- je vsechno mezi tim movable
- pak vsechno posun


kombinujeme obj_map a ground_map do jednoho slovníku a budeme se k nim chovat jako ke stackum věci na sobě

self.map[(x,y)]=list

kde list[0]=id_ground
list[1]=id_obj1
list[2]=id_obj2 
kde id_obj2 je object stacknuty na obj1