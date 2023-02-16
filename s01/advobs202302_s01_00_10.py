#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 16:51:59 (CST) daisuke>
#

# assignment of variables
fruit1     = 'banana'
unitprice1 = 10
quantity1  = 10
fruit2     = 'orange'
unitprice2 = 30
quantity2  = 5
fruit3     = 'apple'
unitprice3 = 60
quantity3  = 2

# calculations
subtotal1 = unitprice1 * quantity1
subtotal2 = unitprice2 * quantity2
subtotal3 = unitprice3 * quantity3

# fancy formatting using formatted string literals
print (f'{"Fruit Name":10s} {"Unit Price":10s} {"Quantity":8s} {"Subtotal":8s}')
print (f'{fruit1:10s} {unitprice1:10d} {quantity1:8d} {subtotal1:8d}')
print (f'{fruit2:10s} {unitprice2:10d} {quantity2:8d} {subtotal2:8d}')
print (f'{fruit3:10s} {unitprice3:10d} {quantity3:8d} {subtotal3:8d}')
