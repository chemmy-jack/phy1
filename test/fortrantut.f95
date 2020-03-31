program fortrantut
	implicit none
	real, parameter :: pi = 3.14159265
	real :: r_num = 1.11111 , r2_num = 2.2222222
	real*8 :: dbl_num = 1.111111111111d+0
	integer :: i_num = 123 
	logical :: logi = .true.
	character (len = 10) :: month
	complex :: com_num = (1.0,2.1)
	print *, "real: ", huge(pi)
	print *, "real: ", r_num
	print *, "real: ", huge(dbl_num)
	print *, "real: ", dbl_num
	print *, "real: ", huge(i_num)
	print *, "real: ", i_num
	print "(3i7)", 21341, 12343, 4357 
	print "(2f8.7)", 1234.2134, 123.45234
	print "(/, 2a8)", "name", "age"

end program fortrantut
