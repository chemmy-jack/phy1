!example.f89
program example
    use :: json_module
    implicit none
    integer, parameter         :: dp = selected_real_kind(15, 307)
    real(kind=dp)              :: t0, dt, tf, mu
    real(kind=dp), allocatable :: x0(:)
    type(json_file)            :: json
    logical                    :: is_found

    ! Initialise the json_file object.
    call config%initialize()

    ! Load the file.
    call json%load_file('config.json'); if (json%failed()) stop

    ! Read in the data.
    call json%get('t0', t0, is_found); if (.not. is_found) stop
    call json%get('dt', dt, is_found); if (.not. is_found) stop
    call json%get('tf', tf, is_found); if (.not. is_found) stop
    call json%get('mu', mu, is_found); if (.not. is_found) stop
    call json%get('x0', x0, is_found); if (.not. is_found) stop

    ! Output values.
    print *, t0
    print *, dt
    print *, tf
    print *, mu
    print *, x0

    ! Clean up.
    call json%destroy()
end program example
