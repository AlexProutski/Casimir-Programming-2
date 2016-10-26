import numpy as np
from scipy import optimize

class Parameter:
    def __init__(self, value, name=''):
        self.value = value
        self.name = name

    def set(self, value):
        self.value = value

    def __call__(self):
        return self.value
    
def gauss(gA,gx0,gs):
    """
    returns the fit function: two gaussians with independent widths, centres and amplitudes.
    A_a * np.exp(-((x-x0_a)/s_a)**2)
    """
    
    A = Parameter(gA,'A')
    x0 = Parameter(gx0,'x0')
    s = Parameter(gs,'s')
    def fitfunc(x):
        return A()*np.exp(-((x-x0())/s())**2)
        
    return p0,fitfunc

def result_dict(p1, cov, info, mesg, success, x, y, p0, fitfunc):
    chisq = 1
    dof = 1
    error_dict = {}
    error_list = []
    params_dict = {}
    
    # print cov, success, mesg, info
    if success:
        chisq = sum(info['fvec']*info['fvec'])
        dof = len(y)-len(p0)
        for i,pmin in enumerate(p1):
            error_dict[p0[i].name] = np.sqrt(cov[i,i])*np.sqrt(chisq/dof)
            #print chisq
            #print dof   
            error_list.append(np.sqrt(cov[i,i])*np.sqrt(chisq/dof))
            params_dict[p0[i].name] = pmin

    result = {
        'success' : success,
        'params' : p1,
        'params_dict' : params_dict,
        'chisq': chisq,
        'dof': dof,
        'residuals_rms': np.sqrt(chisq/dof),
        'reduced_chisq': chisq/dof,
        'error' : error_list,
        'error_dict' : error_dict, 
        'cov' : cov,
        'p0' : p0,
        'fitfunc' : fitfunc,
        'x' : x,
        'y' : y,
        }
    
    return result

def do_fit(x,y,p0,fitfunc):
    """
    Fitting function... thanks diamond
    """
    
    
    # convenient fitting method with parameters; see scipy cookbook for details
    def f(params):
        i = 0
        for p in p0:
            p.set(params[i])
            i += 1

        return y - fitfunc(x)
    
    
    if x is None: x = arange(y.shape[0])
    p = [param() for param in p0]
    
    # do the fit and process
    p1, cov, info, mesg, success = optimize.leastsq(f, p, full_output=True, maxfev=len(x)*100)
    if not success or cov == None: # FIXME: find a better solution!!!
        success = False
        if VERBOSE:
            print('ERROR: Fit did not converge !')
            print('reason: '+str(mesg))
        # return success    #commented out by THT and MA because it bvreaks all old automatic fitting code. 160802
    
    result = result_dict(p1, cov, info, mesg, success, x, y, p0, 
            fitfunc)
    # package the result neatly
    return result
    
def fit_line(ga):
    
    a = Parameter(ga,'a')
    p0 = [a]
    def fitfunc(x):
        return a()*x
    return p0,fitfunc