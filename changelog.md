# day 1 - 14/11

[v0.01]
- basic layout for tabs down with parent child class based structure
- tab toggling 
- basic shelved chatbox

[v0.02]
- refactored to just a customer class that has state for chatbox and draws it based on that state :D
- happy with structure for shelving and opening customer chats from their instances
- sorted bring to front and shelving difference when clicking an opened window
- minimise button
- minimise and bring to front clean flow
- basic customer instance information on chatbox window
- proper bring to front working on the top rect clicked (not any rect chatbox rect that collided with the mouse, i.e. lots of windows are stacked on top of each other)

# day 2 - 15/11
[v0.021]
- fixed issue with blitting surfaces not being wiped at the start of each frame
- added click to move selected chat to mouse pos, realised a few limitations with enough key elements to justify moving to new refactor after first days implementation
    - which tbf planned to do already so good job bud, was the right call! :D

[v1.00]
- day 2 planned refactor to iron out limitations with initial implementation
- base scene ui down and does look beaut with increased size tbf
- toggling tabs basic functionality added
- nailed highlighting on hover and ordering (partially, not yet on click), particularly for ordering almost didnt think id figure out a "cheap" way to do it but i did! :D
- decision for huge overhaul from scratch again and completely nailed moving to click again from start much cleaner oop structure concept


# day 3 
quick notes
- looked at layering, tried to implement realised reason why, may refactor after a test later to accomodate for this (literally just found out what it is and how it works and would require a refactor and since is only day 3 im happy with that)
- improved click to move, now cant have multiple windows selected and held on top of each other, one gets put down before picking up another one, tho this still needs to be improved to do the put down and wait until next frame i.e. next click, before allowing to pick up again 
- added full new orders items dynamically spaced and added to screenw with clickable & highlighting select buttons


# day 3 part 2
quick notes
- started 2nd refactor for chatboxes class with ordering
- works a treat :D
- honestly so chuffed as was rapid too, really feel like my understanding has taken a major leap recently which is amaaaaaaazing
- lets gooooooo, moving and putting down working perfectly AND it does the bring to front now too <3 :D !!!!!!!!!!!!!!!!!!!!!!!!
- fixed chatbox click so it always takes the toppest item which simply required reverse the list and breaking on click :D
- just got the click to drop working properly, i.e. cant pickup and drop in the same frame (for when you click to drop on a position where a window already is)

- so next up to...
- first check over what you've done and lets just do a small refactor for like say if stuff needs to be in functions just so its done now
- then re-add in the old missing functionality with the additional thought for chatbox class and general improvements
    - i.e. hovering and ting
    - honestly from scratch if necessary
- then on to the gameified elements oooOooOOoooo
    - consider redoing the legit first implementation of the items and buttons tho tbf is clean maybe just a baby refactor for now bosh
