# note: incase anyone is reading, this changelog formatting is designed for viewing in vs code and not for .md in github, tho i will soon port it over to the repo .readme 

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
[v3.08-v3.09]
- hover and add menu item with button and highlighting and dynamic surface sizing and button placement
- order number indicator buttons with highlight functionality but not added on click yet
- scrolling order functionality basics
- scrolling only when on new orders tab
- improved that to scrolling when hovering over the actual sidebar
- added highlight to surf when hovered to improve ux further by making it clear the surface has interactivity on hover
- dynamic width add to customer order window button started with basic dynamic width button added 
- added on hover functionality to add to customer btn
- basics of customer select popup added
- added close btn to popup and moved close functionality to the button from the entire window rect
- added names, bg rects, confirm button with hover mouse collision, just more basic setup for the popup window
- selectable names with hover, click, and valid states functionality
- selected order now blitting to selected window, first implementation so got a few things to nail but very happy with everything so far :D

# day 8 
[v3.09]
- blit on click to correct surface
- ui fixes
- setup functionality for blit to surface dynamically, took a few hours
- blit on click working a treat now *i think*, actually just not 100% sure as i cant see the third line (tho can see its position in debug so its there)
    - just need to add scroll to confirm its all working as expected which i think it is, eeeeeee
- technically just the 3rd day on this version and now its all setup will solid class based structure and i actually *get* it, i feel like im flying tbf
    - but a lot of the stuff is just painstakingly long to do regardless as every rect and pos has to be setup dynamically and im doing everything myself
- blit on click now working with its own functionality in its class
- dictionary messages passed and dynamic positions
- currently is sending messages for each item in the basket but thats just while testing
- adding scrolling the selected window on hover, and only works for the selected window even if the mouse is overlapping multiple windows due to oop structure choices <3

# day 9
[v3.10-v3.12]
[v3.10]
- planned upcoming functionality for basket totals, quantities, price info, etc, etc
- added calculating, updating, and drawing current/active basket total price to new sticky bottom bar on orders sidebar 
    - took a while due to amount of tasks required to finish functionality
- added quantities functionality and quantities being taken into consider in active basket price calculation and blits
    - took a while due to planning and figuring out the functionality before implementing
- very happy it with it so far
- updating quantity of items through clicking to add an existing item to the active order basket
- handling the stacking properly for both adding new items or updating quantities of existing ones with new order details dictionary implementation
- now blitting (drawing) the true basket price when sending the order info to the selected customer window on click
- fixed quantity so now it blits the true basket quantity with the price on the payment_window img surface copy now too :D
- adding 3.11 preview now, get some other stuff done, then returning to this later

[v3.11]
- when adding a new or updating the quantity of an existing (will also do delete soon) menu item to the active order there is now a fading highlight rect around the updated / new item for increased visual clarity, a lil bit of added polish, and a small but useful ux improvement in easily being able to revert changes in the rare case you're unsure or forget what you'd just clicked
- added border for window blit (explain better)
- added text bg rect for order number in sidebar but also need to improve/change this (explain better too)

[v3.12]
- looots of sidebar ui changed (+ some additional extras) that ill document tomo
    - basically is customer queue and customer state/status info
- its *really* starting to come along now wow






day 10
[v3.12]
- fixed the highlight on hover to include the new 'sticky' border [10am]
- cleaned up chatbox class
- cleaned up customer class
- starting to flesh out the customer class now (tho likely will refactor once chatboxes are finalised anyways)
- cleaned up parent browser tab and child new orders tab 
- note, started adding more doc strings, mostly to improve the formatting / readability, tho will do mostly going forward but will shortly go back and fill in the missing ones
- fixed bug in main code with write_to_pinboard order of operations
- fixed image copy issue with new customer timer containers
- improving customer state functionality, adding customer sub-states - inactive (completed/cancelled) or active (ordering/preparing/delivering) substates
- adding basic buttons and attributions to main header
- added update customer sub-state functionality to key press 1 
- adding in actual sub-state timers, starting with the ordering sub-state
    - alot of the stuff to add in the sub state, timers, etc for customer taking quite some time due to planning so its clean and implementing properly but has been more than worth it so far so keeping it up
- added cancelled counter and gui element to scene top left info pinbar
- added customer state functionality to move from active to inactive and cancelled substate when not interacted with by the amount of time dictated by their unique schedule trait 
- hooked up the cancelled and active counter functionality for customers and updating states :D
- now drawing the dynamic charging timers for each customer with the percent based on their own unique schedule trait :D
- made timer positions dynamic and gave them their own unique queue to store them so we can easily implement capping the amount to 3
- bar resetting functionality on r key temporarily, which will shortly then move to where it should be which is interacting with the customer
- added blitting name to timer bar too incase i didnt add that
- resolved that one and only bug as it was stupid af, noted below absolutely pmsl, but anyway so now highlight working again as expected 
- added the surface for the customer interact button [8pm]
- removed r to reset each customer timer and replaced with customer window button (just a black surf for now but is fine as am only sorting out the functionality for now)
- convo button sticky setup
- started the basic functionality for wanted_basket concept  
- convo button blitting random item from wanted_basket [9:20pm]
- send payment window to customer now just sending the payment window (not a random selection of items or payment window lol)
    - should get this wiping the sent order asap yanno
- done a load of stuff for setting, resetting, fixing vars for chatlogs update and order states, etc
- ensured chatbox blit is working as expected and is still printing after the customer cancels, plus for multiple instances with their own seperate wanted orders and blitting to their own windows seperately, hover still working, etc - just standard things to make sure everything is still as expected, which it is! :D



day 11
- was travelling to sheffield but did work on this for about half the day
- didnt make notes tho, will try to go back and fill this in a bit later on today tho
- basically just started the new preparing orders tab tho
- and the basic functionality for the map popup
- and then the start of customer paid functionality too 
- improved new tab structure a tad by abstracting out some functionality 



day 12
[v3.14]
- configured ticks timer to set customer to paid after a short amount of time and update their payment window img to show this too
- state resetting
- cleaned up code a tad to remove some unnecessary repetion 
- added removing the ordering timer when the customer has paid
- added a new surface / section to the new preparing tab for the queueing customers
- moved the button to this new top surface and repositioned and resized so its dynamic sized and in a more logical location
- now blits a yellow 'card' for each customer in the new preparing tabs - preparing customers top bar
- added dynamic positioning to the preparing customer cards
- added simple name text blit to the prep customer cards
- top left sidebar now flows from ordering state to preparing state correctly (tho only tested for 1 customer for now tbf), required adding new ordering state + preparing state too and linking it up all
- added temp click to map popup to select a store (well just closes for now but adding that in next) [friday-21:15]
- temp functionality to send preparing order to store on button press (just removes from the queue for now but doing that next) 

[took-saturday-off-for-once]
- did do like an hour tbf but hardly worth including

day 13
[v3.15]
- new rotate around center
- new rotation image handler
- timer container now rotating based on wait time chargebar percentage
- dynamic colour change on chargebar rgb based on percentage (green to orange to red)

# note
- really need to get a new version out quickly and a vid update btw


# random to do
- need to add overview to main header (obvs need in readme too, could also bang in its own file too, along with this changelog, etc)

# generalised to do
- add in button to loop through the customers chatlog stuff
- msg ui timers and customer screen gui stuff
- general minor things as per notes
- then really just ironing out all that functionality :D


