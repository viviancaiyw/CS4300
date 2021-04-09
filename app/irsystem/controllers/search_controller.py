from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from flask_login import login_required

project_name = "Steamy Reviews: Game Recommendation Engine"
net_id = "Chang Wei: cw887, Qichen Hu: qh75, Yuwen Cai: yc687, Yitian Lin: yl698"

@irsystem.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



