import timeit
print("running c_opt")
c_opt = timeit.timeit('all_funcs()', setup='from asc2log_c_opt import all_funcs', number=1)
#print("running original_py")
#original_py = timeit.timeit('all_funcs()', setup='from asc2log import all_funcs', number=1)

#print("Cython speedup by " + str(((original_py/c_opt)-1)*100) + "%")
