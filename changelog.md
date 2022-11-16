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
