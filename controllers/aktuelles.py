def eintrag():
    if request.args and request.args[0] :
        announcement_id = request.args[0]
        n = ompdal.getAnnouncementSettings(announcement_id).as_list()

        t = list(filter(lambda e: e['locale'] == locale and e['setting_name'] == 'title', n))
        title = XML(t[0]['setting_value']) if t else ''

        dl = list(filter(lambda e: e['locale'] == locale and e['setting_name'] == 'description', n))
        description = XML(dl[0]['setting_value']) if dl else ''
        if len(description) > 0:
            return locals()
        else:
            raise HTTP(400, T('No Content'))

    else:
        raise HTTP(400, T('No Content'))