# Screening_Task-1


A room slot booking Django project havinf the following functionalities :-

1.Authenticate the user

  -Allow new users to sign up

  -Allow existing users to sign in

2.Users are of two types: Room Manager & Customer.

3.Room Manager should be able to define the number of Rooms available.

4.A Room Manager can define the Time Slots for which a Room is available every day.

5.Time slots are constantly recurring.

6.A Customer can book a Room and a corresponding Time Slot, once booked, the Room cannot be booked by another Customer for that Time Slot.

7.Only an authenticated user to Book or set Rooms

8.A Customer able to book a Room ‘x’ days in advance. Room Manager should be able to define the number of days ‘x’.

9.Only Room Manager can add, delete or change his own number of Rooms and Time Slots.

10.A Customer able to view and delete only his own bookings

11.Room Manager able to view a summary of all bookings, occupancies and occupant customer details.

12.The customer able to see all of his own (past and future) bookings, occupancies and room manager.


Technologies/Libraries to use:

1.Django
2.Python 
3.HTML
4.Git





 yaksh.fossee.in Details :-
 email - diptanshumittal@gmail.com
 username - diptanshu18232
 
 
 
 
 Some assumptions made :-
 
 1.You can only book the slot for one day only.
 
 
 2.The duration should be  multiple of 60mins and for slots in midnight, you have to do two separate bookings for both the days 
 
 
 3.The slots will merge itself automatically if the rooms with deatils are added and overlap with the existing slot of the same room 
 
 4.In add room the upto date means the date by upto which the slots are available daly upto that date and the buffer days means the advance days the customer is able to book the slot
 
 
 
