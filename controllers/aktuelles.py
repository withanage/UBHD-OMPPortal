import ompformat

def eintrag():
    if request.args and request.args[0] :
        announcement_id = request.args[0]

        n = ompdal.getAnnouncementWithSettings(announcement_id)

        title = n.get('title', {}).get(locale, '')

        description = XML(n.get('description', {}).get(locale, ''))
        short_description = XML(n.get('descriptionShort', {}).get(locale, ''))

        date = ompformat.dateToStr(n['date_posted'], locale)

        archive = ompdal.getAnnouncementsByPressGroupedByYearAndMonth(press_id, locale)

        return locals()
        #if len(description) > 0:
        #    return locals()
        #else:
        #    raise HTTP(404, T('No Content'))

    else:
        raise HTTP(404, T('No Content'))

def archiv():
    return dict()
