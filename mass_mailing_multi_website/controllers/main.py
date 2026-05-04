import logging

from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class Website(Website):
    @http.route("/website/get_suggested_links", type="json", auth="user", website=True)
    def get_suggested_link(self, needle, limit=10):
        current_website = request.website
        result = super().get_suggested_link(needle, limit)
        _logger.error("HERE: current_website ")
        _logger.error(current_website)
        # Add the website url to the beginning of urls so later it can not be set wrong
        if "matching_pages" in result:
            _logger.error("HERE: result ")
            _logger.error(result)
            for item in result["matching_pages"]:
                if "domain" in current_website:
                    item["value"] = current_website["domain"] + item["value"]
                    if "label" in item and item["label"].startswith("/"):
                        item["label"] = current_website["domain"] + item["label"]
        if "others" in result:
            for pages in result["others"]:
                for item in pages["values"]:
                    if "domain" in current_website:
                        item["value"] = current_website["domain"] + item["value"]
                    if "icon" in item and item["icon"].startswith("/"):
                        item["icon"] = current_website["domain"] + item["icon"]
                    if "label" in item and item["label"].startswith("/"):
                        item["label"] = current_website["domain"] + item["label"]
        return result
