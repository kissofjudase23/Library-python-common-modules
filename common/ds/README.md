# Data Structure

## Reference
- [Big-O Complexity Chart](http://bigocheatsheet.com/)

## Table of Contents
- [Linked List](#linked-list)
- [Hash Table](#hash-table)
- [Stack](#stack)
- [Queue](#queue)
- [Cache](#cache)
  - [LRU](#lru-cache)


## Linked List
- Average and Worst
- 
    |                              | Search | Push_front | Push_back | Remove Node |
    |------------------------------|--------|------------|-----------|-------------|
    | Singly Linked List with tail | O(n)   | O(1)       | O(1)      | O(n)        |
    | Doubly Linked List with tail | O(n)   | O(1)       | O(1)      | O(1)        |

## Hash Table
- Average
 
    |            | Set  | Get  | Delete |
    |------------|------|------|--------|
    | Hash Table | O(1) | O(1) | O(1)   |

- Worst
 
    |            | Set  | Get  | Delete |
    |------------|------|------|--------|
    | Hash Table | O(n) | O(n) | O(n)   |

## Stack
- Average and Worst

    |       | Push | Pop  | Search|
    |-------|------|------|-------|
    | Stack | O(1) | O(1) | O(n)  | 

## Queue
- Average and Worst
 
    |       | Add  | Pop  | Search|
    |-------|------|------|-------|
    | Queue | O(1) | O(1) | O(n)  | 


## Cache
### LRU Cache
- Doubly Linked List + Hash Table

    |            | Set  | Get  | Delete |
    |------------|------|------|--------|
    | LRU Cache  | O(1) | O(1) | O(1)   |
