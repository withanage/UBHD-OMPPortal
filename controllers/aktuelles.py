import ompformat
import datetime
import calendar


def index():
    announcements = ompdal.getAnnouncementsByPress(press_id)
    if announcements:
        return redirect(URL('eintrag', args=[announcements[0].announcement_id]))
    else:
        return HTTP(404, T("No announcements"))


def eintrag():
    if request.args and request.args[0]:
        announcement_id = request.args[0]

        n = ompdal.getAnnouncementWithSettings(announcement_id)

        title = XML(n.get('title', {}).get(locale, ''))

        description = XML(n.get('description', {}).get(locale, ''))
        short_description = XML(n.get('descriptionShort', {}).get(locale, ''))

        date = ompformat.dateToStr(n['date_posted'], locale)

        archive = ompdal.getAnnouncementsByPressGroupedByYearAndMonth(press_id, locale)

        current_year = datetime.datetime.now().year

        # Helper functions for the template
        strip_tags = ompformat.strip_tags

        def month_to_literal(month_int):
            return T(calendar.month_name[month_int])

        return locals()
        # if len(description) > 0:
        #    return locals()
        # else:
        #    raise HTTP(404, T('No Content'))

    else:
        raise HTTP(404, T('No Content'))
