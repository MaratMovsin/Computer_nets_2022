import numpy as np

def control_sum(byte_arr):
    if byte_arr.shape[0]%2:
        byte_arr = np.hstack((np.zeros(1), byte_arr))
    byte_mat = byte_arr.reshape(-1, 2)
    return 65535 - ((byte_mat @ np.array([256,1])).sum() % 65536)
    
def check_sum(byte_arr, c_sum):
    if byte_arr.shape[0]%2:
        byte_arr = np.hstack((np.zeros(1), byte_arr))
    byte_mat = byte_arr.reshape(-1, 2)
    return (((byte_mat @ np.array([256,1])).sum() + c_sum) % 65536 == 65535)

def test_1():
    arr = np.array([2, 3, 5, 0])
    assert (control_sum(arr)==63740)
    assert (check_sum(arr, 63740)==True)
    assert (check_sum(arr, 8)==False)
    
def test_2():
    arr = np.array([34, 43, 23, 96, 158, 148])
    assert (control_sum(arr)==10208)
    assert (check_sum(arr, 10208)==True)
    
def test_3():
    arr = np.array([1, 2, 3])
    assert(control_sum(arr)==65019)

test_1()
test_2()
test_3()
