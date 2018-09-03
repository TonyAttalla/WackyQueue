"""
# Copyright Nick Cheng, Tony Attalla 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Tony Attalla
# 1003974158
# attalla8
#+
# Do not add import statements or change the one above.
# Write your WackyQueue class code below.

from wackynode import WackyNode


class WackyQueue:

    def __init__(self):
        '''(WackyQueue)-> None
        Creates a new WackyQueue that starts off 
        with no elements
        '''
        # Represenation invariant:
        # the WackyQueue is represented with two linked lists
        # of WackyNodes. the odd list head is the WackyNode
        # in the linked list pointing to every odd WackyNode
        # beginning with the first. the even list head is
        # the second object pointing to every even WackyNode
        # beginning with the second. Each WackyNode contains space
        # for a priority, an item, and a pointer to another
        # wackynode. The Queue behaves in such a way that
        # Nodes with higher priorities are ahead of nodes
        # with lower priorities in the Queue. When items are
        # inserted with the same priority, the ones inserted
        # earlier are earlier in the Queue.

        # initialize both the oddListHead and evenListHead as local instance
        # variables that start off as none, because we haven't added any
        # objects yet
        self._oddListHead = None
        self._evenListHead = None

    def insert(self, obj, priority):
        '''(WackyQueue, obj, int) -> None
        Inserts an item named obj with priority given into the 
        WackyQueue. If an item already exists with the same priority,
        the earlier item goes first in the WackyQueue.
        The way insert functions is that when we insert an element, all
        the elements that come after it are swapped from their current
        linked list to the other one. Let's take a look at an example:
        Odd List: [A] -> [D]-> [F]->[H]
        Even List: [B] -> [E] -> [G]
        Now let's say we want to insert C, the lists Become:
        Odd List: [A]->[C]->[E]->[G]
        Even List: [B]->[D]->[F]->[H]
        Notice how elements {D, F, H} that were originally in the odd list
        swapped to the even list, and elements {E,G} that were originally in
        the even list swapped to the odd list. In the code, we usually only have
        to make 1 swap however, because D would point to F which points to H, etc...
        and E would point to G, etc....
        '''

        # creating a new node that we're gonna insert into either
        # the odd linked list or the even linked list
        Node = WackyNode(obj, priority)
        # initializing some variables to keep track of the current
        # objects in the even and odd lists we're looking at.
        currentOdd, currentEven = self._oddListHead, self._evenListHead

        # Let's also initialize some variables to keep track of the previous
        # values, because sometimes we'll need to modify them and the
        # list is only singly linked
        previousOdd, previousEven = None, None
        # make a flag variable so that we know when to stop the loop
        # if we've found the correct spot to insert
        spotFound = False
        # in the case where the head of the even list is none (IE: empty)
        if currentEven == None:
            # in case the odd and even list are none (so the queue is completely empty)
            # we need to make the node the head of the odd list (because its the first element)
            # and indicate that we've found a spot
            if currentOdd == None:
                self._oddListHead = Node
                spotFound = True
            else:
                # now we branch off into two other cases
                # if the element has priority greater than the
                # largest element and the lists arent empty, we need
                # to swap the values of the even and odd lists, and
                # set the node to the highest value
                if priority > self._oddListHead.get_priority():
                    self._evenListHead = self._oddListHead
                    self._oddListHead = Node
                    spotFound = True
                # if the Queue contains only 1 element, we can
                # set the head of the even list as the node
                # and change the flag
                elif priority <= self._oddListHead.get_priority():
                    self._evenListHead = Node
                    spotFound = True
        # in the case where the element to insert is the largest in the queue
        # and the list isn't empty we need to swap the heads of the lists
        # and set the item as the first in the Queue, also make sure
        # that the new item points to the old head of the odd list
        if currentOdd != None and currentEven != None:
            if priority > currentOdd.get_priority():
                (self._oddListHead, self._evenListHead) = (
                    self._evenListHead, self._oddListHead)
                Node.set_next(self._oddListHead)
                self._oddListHead = Node
                spotFound = True
        # initialize a counter so that we know whether to increment through the odd list or the
        # even list
        counter = 0
        # the following loop tries to find a spot to place the new element
        # while we're not at the end of both lists and the flag hasn't
        # been set to true(which would mean that we've already found a spot)
        while currentOdd != None and currentEven != None and not spotFound:
            # the following cases account for the cases where we're at the end
            # of one or both lists
            if currentEven.get_next() == None:
                if currentOdd.get_next() == None:
                    # if we're at the end of both lists and the element is less than both the last
                    # elements in each list, we need to set the last element in the WackyQueue to the
                    # node, and change the flag
                    if priority <= currentOdd.get_priority() and priority <= currentEven.get_priority():
                        currentOdd.set_next(Node)
                        spotFound = True
                # if we're at the last element in the even list but there's still an element in the odd list
                # we need to set the element to the next even and change the flag
                else:
                    if priority <= currentOdd.get_next().get_priority():
                        currentEven.set_next(Node)
                        spotFound = True

            # in the case where we're looking in the middle of the lists and we still haven't found a place to
            # insert our new element
            if spotFound == False:
                # in the case where our current element is between the element we're looking at in the even
                # list and odd list, we need to link the element inside the even list while switching the even
                # and odd elements that come after it.In all cases, change the flag
                if currentEven.get_priority() <= priority <= currentOdd.get_priority():
                    if previousEven != None:
                        previousEven.set_next(Node)
                    Node.set_next(currentOdd.get_next())
                    currentOdd.set_next(currentEven)
                # in the case where the even element is the head, we need
                # to set the head of the even list to the new element.
                    if currentEven == self._evenListHead:
                        self._evenListHead = Node
                    spotFound = True
                # this case is also where the current element is between our current even and odd element, but the odd
                # element is greater and the even element is smaller, we perform the exact same operations as above, but
                # using the opposite list as above. we also dont need to do any checking for if we're dealing with the
                # heads of the lists because we would have dealt with this outside the while loop.
                if currentOdd.get_priority() <= priority < currentEven.get_priority():
                    previousOdd.set_next(Node)
                    Node.set_next(currentEven.get_next())
                    currentEven.set_next(currentOdd)
                    spotFound = True
            # the following statements increment our values to check in the odd and even lists
            # we need to make sure that we're not just looking at the n'th elements in each list
            # because we need to compare the nth value of the odd list with the nth value in the even
            # list, and then the nth value of the odd list with the n+1th value in the even list, etc...
            # so we make it so that on every even number, the values in the odd list will be incremented,
            # and on every odd number, the values in the even list will be incremented. Obviously, increment
            # the counter itself as well
            if counter % 2 == 0:
                previousOdd = currentOdd
                currentOdd = currentOdd.get_next()
            else:
                previousEven = currentEven
                currentEven = currentEven.get_next()
            counter += 1
    # QED

    def changepriority(self, obj, priority):
        '''(WackyQueue, obj, int) -> None
        Changes the priority of the first instance
        of obj to given priority
        '''
        # make some variables so we can keep track of the
        # current elements in the odd and even list we're
        # looking at. Start at the head of both lists
        currentEven, currentOdd = self._evenListHead, self._oddListHead
        # We also need to make variables for the
        # previous nodes because the list is only singly linked
        previousEven, previousOdd = None, None
        # a flag we can use to indicate whether we've already found the first
        # instance of an item
        itemFound = False
        # while we havent yet found an item and we're not at the end of the
        # linked list, keep looking for the item
        while not itemFound and currentEven is not None or currentOdd is not None:
            # if the item is in the odd linked list
            if currentOdd.get_item() == obj:
                # this deals with the case where the item is the head of the odd list
                # we'll need to change the head of the odd list to the even item we're
                # looking at and the head of the even item to the next odd item
                if currentOdd == self._oddListHead:
                    (self._oddListHead, self._evenListHead) = (
                        currentEven, currentOdd.get_next())
                else:
                    # if we're not looking at the head, we simply have to swap the order of the odd
                    # and even lists, as well as remove the element
                    previousOdd.set_next(currentEven)
                    previousEven.set_next(currentOdd.get_next())
                # change the flag to true
                itemFound = True
            # now we check for the same conditions as above except we have a case
            # where the odd list has one more element then the even list, so we'll
            # run into problems when trying to call .get_item() on nonetype
            if currentEven != None and itemFound == False:
                # if the element we're looking for is found in the even linkedlist
                if currentEven.get_item() == obj:
                    # this is the case where the element is contained in the even list
                    if currentEven == self._evenListHead:
                        # if the element is the head of the even list, just set the
                        # head of the even list to the next odd item, effectively
                        # removing the item
                        self._evenListHead = currentOdd.get_next()
                    else:
                        # otherwise, set the current index to the next
                        # value in the odd list
                        previousEven.set_next(currentOdd.get_next())
                    if currentEven != None:
                        # if the element is not found at the end of the list we
                        # need to remove the element by setting the next object
                        # value to the next even object
                        currentOdd.set_next(currentEven.get_next())
                    else:
                        # if the element is found at the end of the list
                        # we can just set the current object to None
                        currentOdd.set_next(None)
                    # set the flag to true
                    itemFound = True

            # increment the current nodes that we're looking at
            previousEven = currentEven
            previousOdd = currentOdd
            if currentEven != None:
                currentEven = currentEven.get_next()
            else:
                currentEven = None
            currentOdd = currentOdd.get_next()
        # if we've actually found an item, reinsert the item now that
        # we've removed it with the given priority
        if itemFound == True:
            self.insert(obj, priority)

    def negateall(self):
        '''(WackyQueue) -> None
        A function to reverse all the elements in a WackyQueue by
        multiplying their priority by -1 and updating the WackyQueue
        after. negateall accesses a helper function titled reverselist
        that takes in the head of a linked list, reverses the linked list
        and returns a tuple containing the size of the new linked list 
        and the head of the new, reversed linked list
        '''
        # using the reverseList helper function, let's get back
        # the pointer to the oddList and the size of the list
        (oddHead, oddSize) = self.reverselist(self._oddListHead)

        # using the reverseList helper function, let's get back
        # the pointer to the evenList and the size of the list
        (evenHead, evenSize) = self.reverselist(self._evenListHead)
        # if the sizes are equal, we need to swap the head of the
        # even list and odd list
        if evenSize == oddSize:
            (self._oddListHead, self._evenListHead) = (evenHead, oddHead)

        # if the sizes are different, we can keep the heads the same,
        # we just need to assign them to our instance variables because
        # the helper function returns the heads
        else:
            (self._evenListHead, self._oddListHead) = (evenHead, oddHead)

    def reverselist(self, head):
        '''(WackyQueue, WackyNode) -> (WackyNode,int)
        Reverses the linked list that's passed into it with
        given head and returns a tuple containing the size of 
        the new linked list and the head of the new linked list
        '''
        # A variable for the new head of the reversed list we want to return
        newHead = None
        # a variable for the head that we're currently looking at (This won't always
        # be the  same as the head given as a parameter, because as we remove elements from
        # the list, we're gonna need to assign a new head)
        currentHead = head
        # a variable to keep track of the size of the list we're dealing with
        size = 0
        # while we haven't yet reached the end of the list
        while currentHead != None:
            # set the priority of the item we're currently looking at to the same priority
            # *-1, essentially making it so that all the largest elements become the smallest
            # elements, and vice-versa
            currentHead.set_priority(currentHead.get_priority()*-1)
            # increment our size variable for every element we go through
            size += 1
            # make a temporary variable to store the next element we want to look at
            # since we'll lose access to it after we cut the head off
            nextElement = currentHead.get_next()
            # update our new linked list by making the currentHead point
            # to the element we're currently looking at
            currentHead.set_next(newHead)
            # update the head of the new linked list
            newHead = currentHead
            # increment the element we're looking at
            currentHead = nextElement
        # return a tuple containing the head of the reversed linked list and
        # the size of the new linked list
        return (newHead, size)

    def getoddlist(self):
        '''(WackyQueue) -> WackyNode
        Returns the head of the linked list of WackyNodes containing all
        the odd elements
        '''
        # Return the head of the oddList
        return self._oddListHead

    def getevenlist(self):
        '''(WackyQueue) -> WackyNode
        Returns the head of the linked list of WackyNodes containing all
        the even elements
        '''
        # Return the head of the evenList
        return self._evenListHead

    def extracthigh(self):
        '''(WackyQueue) -> WackyNode
        Returns the head of the element with the greatest priority
        in the WackyQueue
        REQ: WackyQueue cannot be empty
        '''

        # A variable called nextItem to store the value
        # of the item that comes after the highest
        nextItem = None
        # we'll have to set the second element to the value of the
        # first element in the even list because we're gonna take
        # the first element out
        nextItem = self._oddListHead.get_next()
        # we know the item we want to return is the first item in the queue, which is odd
        # so we'll call get_item() on the head of the oddlist
        highest = self._oddListHead.get_item()
        # now we need to swap the even and oddlist heads because item n will become
        # n-1, item n-1, will become item n-2, etc... so odds will become even and
        # evens will become odd
        self._oddListHead = self._evenListHead
        # set the value of the head of the even list to the item that came after
        # the highest item in the odd list
        self._evenListHead = nextItem
        # return the highest element
        return highest

    def isempty(self):
        '''(WackyQueue) -> Boolean
        Returns a boolean indicating whether or not the WackyQueue is 
        empty (contains no elements)
        '''
        # We know that if the head of the odd list is none. We don't
        # need to check if the even list head is none because the
        # odd list contains the first element, obviously if there
        # is no first element, there can't be a second element, etc...
        return (self._oddListHead is None)