import gatehandlers.home as home
import gatehandlers.errors as errors
import gatehandlers.examples as examples
import gatehandlers.fontawesome as fontawesome
import gatehandlers.developer as developer
import gatehandlers.project as project
import gatehandlers.testsp as testsp
import gatehandlers.reqs as reqs
import gatehandlers.examples as examples

from org.transcrypt.stubs.browser import __pragma__

gates = {
    'home': home.Index,
    'examples': examples.Index,
    'fontawesome': fontawesome.Index,
    'developer': developer.Index,
    'project': project.Index,
    'test_phanterpwa': testsp.Index,
    'check_requeriments': reqs.Index,
    'examples': examples.Index,
    404: errors.Error_404,
    401: errors.Error_401,
    403: errors.Error_403
}
