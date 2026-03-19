from flask import Blueprint,request,render_template

from services.search_service import search_videos

search_routes=Blueprint("search",__name__)

@search_routes.route("/search")
def search():

    q = request.args.get("q", "")
    category_param = request.args.get("categories", "")
    if category_param:
        category_ids = [int(x) for x in category_param.split(",")]
    else:
        category_ids = []

    videos = search_videos(q, category_ids)

    return render_template("search.html", videos=videos, q=q)