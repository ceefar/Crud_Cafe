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
- fixed issue with title being blit on top of moving chatboxes due to layering / order of operations
- xray border hover ting, might change to use layers tho 
- text and improved hover border

- so next up to...
- first check over what you've done and lets just do a small refactor for like say if stuff needs to be in functions just so its done now
- then re-add in the old missing functionality with the additional thought for chatbox class and general improvements
    - i.e. hovering and ting
    - honestly from scratch if necessary
- then on to the gameified elements oooOooOOoooo
    - consider redoing the legit first implementation of the items and buttons tho tbf is clean maybe just a baby refactor for now bosh


# day 4
[v2.03]
- new ver for playground stuff
- implemented minimise button with shelving and opening, dynamic shelved positions and reset opened positions
- im in love <3
- need to add from notes tbf did a lot more than this lol


# day 5
[v3.01-huge-refactor]
- decided on refactor to really nail things in terms of cleanliness of the code x functionality
- working a treat so far just readded properly clean af layering system that reorders everything after performing a move to front operation
- clean hovering done and finally fixed a lot of issues that i had with the initial implementation <3
- clicking and move working
- clicking and move now done via top bar only
- fixed issue where could click on another top bar that was underneath, and therefore not the active highlighted one
- now when click top title bar the window is selected at the exact mouse pos <3
- added extra window image state for when clicked and selected for move the highlight colour is different for visual clarity


# day 6
[v3.04-v3.05+]
- unshelving
- unshelving rect and image fixes for instance states
    - pretty complicated tbf as when each window changes its image, as the dimensions change requires re-drawing all the rects, and repositioning if necessary, thankfully code so far has been very robust and things have surprisingly just worked as expected by in large :D
- shelved highlighting
- big note but have noticed that when unshelving the positions are ordered based on how they were instantiated and not when they were added to the active list
    - i *may* come back to fix this one however for this imo it is prefectly fine, the desire is to just ensure you have the desired window on top
        i.e. from a ux perspective it is still good and is barely noticeable, it just is to me as im coding it lol
    - but tbf also may just take a look at this when doing dropping windows as there likely is a reasonably short solution in there too
- click unshelving, so clean im in love <3 <3 <3
- same with minimising and setting initial cascading offset positions, so clean and easy to implement due to good design patterns <3 <3 <3
- trying to do new orders stuff on a 3.06 now
- extended new orders child class to override the Browser_Tab parent update() function to include functionality for the orders sidebar :D <3


# day 7
- hover and add menu item with button and highlighting and dynamic surface sizing and button placement
- order number indicator buttons with highlight functionality but not added on click yet
- scrolling order functionality basics
- scrolling only when on new orders tab
- improved that to scrolling when hovering over the actual sidebar
- added highlight to surf when hovered to improve ux further by making it clear the surface has interactivity on hover
- dynamic width add to customer order window button started with basic dynamic width button added 
- added on hover functionality to add to customer btn
- basics of customer select popup added