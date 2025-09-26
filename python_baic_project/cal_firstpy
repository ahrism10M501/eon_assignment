def adder(num1, num2):
    return num1 + num2

def myf(x):
    form = x**2+2*x+5
    print(form)
    return form

from math import sqrt, asin, pi

def pythagoras(width, height):
	hypotenuse = sqrt(width**2+height**2)
	radian = asin(height/hypotenuse)
	return (hypotenuse, radian)

print(f"3 + 4 = {adder(3, 4)}")
print(f"f(x) = x^2+2x+5 => f(5) = {myf(5)}")
print(f"밑변의 길이 3, 높이 4 일 때, 빗변의 길이 {pythagoras(3, 4)[0]}, 각도 {pythagoras(3, 4)[1]}rad, {pythagoras(3, 4)[1]/pi*180}˚")

width, height = (3, 4)
value = pythagoras(width, height)
print(f"밑변의 길이 {width}, 높이 {height} 일 때, 빗변의 길이 {value[0]}, 각도 {round(value[1],4)}rad, {round(value[1]/pi*180)}˚")