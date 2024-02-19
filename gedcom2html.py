import codecs
import os
import shutil
import string

from gedcomParser import GedcomParser


def calc_color(type, level=0, gender='M'):
    level_max = 10.0;
    if type == 0:  # not related
        c = '#aaa'
    elif type == 1:  # home_person
        c = '#00f'
    elif type == 2:  # parent
        x = 10 + 240 * (1 - (level / level_max))
        c = '#%s0000' % format(int(x), '02x').upper()
    elif type == 3:  # child
        x = 10 + 240 * (1 - (level / level_max))
        c = '#00%s00' % format(int(x), '02x').upper()
    else:
        c = '#000'  # error
    return c


class Html:
    def __init__(self, g, p, all_persons, options):
        self.gedcom = g
        self.person = p
        self.options = options
        self.all_persons = all_persons
        for id, p2 in self.all_persons.items():
            self.all_persons[id].color = calc_color(0)
        p.color = calc_color(1)
        self.__fid = codecs.open('HTML/' + p.link, encoding='utf-8', mode='w')
        self.write_header()
        self.__fid.write("<div class='row'>\n")
        self.write_person()
        self.write_parents()
        self.write_families()
        self.write_siblings()
        self.__fid.write("</div><!-- row -->\n")

    def __del__(self):
        self.__fid.close()

    def write_header(self):
        self.__fid.write("<!DOCTYPE html>\n")
        self.__fid.write("<html lang='en'>\n")
        self.__fid.write("<head>\n")
        self.__fid.write("<title>%s</title>\n" % self.person.short_name)
        self.__fid.write(
            "<meta name=\"description\" content=\"%s\" /><meta name='viewport' content='width=device-width, initial-scale=1.0'>\n" % self.options.title)
        self.__fid.write("<meta http-equiv='Content-Type' content='text/html;charset=utf-8' />\n")
        self.__fid.write("<link rel='stylesheet' type='text/css' href='css/bootstrap.min.css' />\n")
        self.__fid.write("<link rel='stylesheet' type='text/css' href='css/font-awesome.min.css' />\n")
        self.__fid.write(
            "<link rel='stylesheet' type='text/css' href='css/gedcom2html.css' media='screen, projection, print' />\n")
        self.__fid.write("<script type='text/javascript' src='js/jquery-3.1.1.min.js'></script>\n")
        self.__fid.write("<script type='text/javascript' src='js/d3.v4.min.js'></script>\n")
        self.__fid.write("<script type='text/javascript' src='js/bootstrap.min.js'></script>\n")
        self.__fid.write("<script type='text/javascript' src='js/gedcom2html.v4.js'></script>\n")
        self.__fid.write("</head>\n")
        self.__fid.write("<body>\n")
        self.__fid.write(
            "<div class='page-header'><a href='index.html'><span class='fa fa-home'></span> %s</div></a>\n" % self.options.title)
        self.__fid.write("<div class='container'>\n")

    def __write_family(self, id, level):
        white_space = '   ' * (level + 1)
        for index, family in enumerate(self.all_persons[id].family):
            # SPOUSE
            show_spouse = 0
            if len(family.spouse_id) > 0 and level == 0:
                show_spouse = 1
            if show_spouse:
                if index == 0:
                    self.__fid.write("<ul class='tree'>\n")
                if len(family.spouse_id) > 0:
                    self.__fid.write("   <li><i class='fa fa-heart' style='color:#faa'></i> %s\n" % (
                        self.all_persons[family.spouse_id].string_long))
            # CHILDREN
            if len(family.child_id) > 0:
                if level == 1:
                    self.__fid.write("%s<ul class='tree' id='ul_children_%s'>\n" % (white_space, id))
                else:
                    self.__fid.write("%s<ul class='tree'>\n" % (white_space))
                for child_id in family.child_id:
                    arrow = ""
                    self.all_persons[child_id].color = calc_color(3, level, self.all_persons[child_id].gender)
                    if level == 0:
                        if len(self.all_persons[child_id].family) > 0:
                            arrow = "<i class='fa fa-arrow-circle-right' id='children_%s' onclick='toggle_tree(\"children_%s\")'></i>" % (
                                child_id, child_id)
                    self.__fid.write("%s   <li>%s" % (white_space, arrow))
                    self.__fid.write(" %s\n" % (self.all_persons[child_id].string_long))
                    if len(self.all_persons[child_id].family) > 0:
                        self.__write_family(child_id, level + 1)
                self.__fid.write("%s</ul>\n" % white_space)

    def write_person(self):
        self.__fid.write("<div class='well'>\n")
        self.__fid.write(f"<h1>{self.person.string_short}</h1>\n")
        self.__fid.write("<ul>\n")
        # ----- Birth info -----
        birth_date = self.person.birth_date.strftime('%d/%m/%Y') if self.person.birth_date is not False else "?"
        birth_town = self.person.birth_place.split(', ')[0] if self.person.birth_place is not False and len(
            self.person.birth_place.split(', ')) > 0 else "?"
        birth_department = self.person.birth_place.split(', ')[2] if self.person.birth_place is not False and len(
            self.person.birth_place.split(', ')) > 2 else "?"
        self.__fid.write(f"<li>"
                         f"Né le {birth_date} "
                         f"à {birth_town} ({birth_department})"
                         f" </li>\n")

        # ----- Spouse info -----

        # self.__fid.write(f"<li>"
        #                  f"Marié le {self.person.current_marriage['date']}"
        #                  f"à {self.person.current_marriage['place']}"
        #                  f"avec {self.person.current_marriage['spouse_name']}"
        #                  f" </li>\n")
        # if len(self.person.nick_name)>0:
        self.__fid.write(f"<li>Prenom: {self.person.first_name}\n")
        if len(self.person.notes) > 0:
            self.__fid.write("<li>%s\n" % self.person.notes)
        self.__fid.write("</ul>\n")
        self.__fid.write("</div>\n")

    def write_parents(self):
        if len(self.person.parent_id) > 0:
            self.__fid.write("<h2>Parents</h2>\n")
            self.__fid.write("<ul class='tree'>\n")
            for parent_id in self.all_persons[self.person.id].parent_id:
                p = self.all_persons[parent_id]
                # if len(self.all_persons[p.id].parent_id) > 0:
                #    arrow = f"<i class='fa fa-arrow-circle-right' id='parent_{p.id}'></i>"
                self.__fid.write("   <li>")
                self.__fid.write(f" {p.string_long}\n")
                self.all_persons[p.id].color = calc_color(2, 0, self.all_persons[p.id].gender)
            self.__fid.write("</ul>\n")

    def write_families(self):
        if len(self.all_persons[self.person.id].family) > 0:
            self.__fid.write("<h2>Enfants</h2>\n")
            self.__write_family(self.person.id, 0)

    def write_siblings(self):
        list_of_child_ids = []
        for parent_id in self.person.parent_id:
            for family in self.all_persons[parent_id].family:
                for child_id in family.child_id:
                    if child_id not in list_of_child_ids:
                        if child_id != self.person.id:
                            list_of_child_ids.append(str(child_id))
        if len(list_of_child_ids) > 0:
            self.__fid.write("<h2>Siblings</h2>\n")
            self.__fid.write("<ul>\n")
            for child_id in list_of_child_ids:
                self.__fid.write("<li>%s\n" % (self.all_persons[child_id].string_long))
            self.__fid.write("</ul>\n")

    # def __write_json_line(self, s, level):

    def __write_json_for_fan_chart_ancestors(self, id, level):
        p = self.all_persons[id]
        white_space = '   ' * level
        white_space2 = '   ' * (level - 1)
        self.__fid.write('%s{\n' % white_space2)
        self.__fid.write('%s"name": "%s",\n' % (white_space, p.shortest_name))
        # self.__fid.write('%s"generation": "%d",\n'% (white_space, level))
        self.__fid.write('%s"gender": "%s",\n' % (white_space, p.gender))
        self.__fid.write('%s"color": "%s",\n' % (white_space, p.color))
        self.__fid.write('%s"href": "%s",\n' % (white_space, p.link))
        # if p.birth_date == False:
        # self.__fid.write('%s"born": "",\n' % (white_space))
        # else:
        # self.__fid.write('%s"born": "%s",\n'% (white_space, '{0.year:4d}'.format(p.birth_date)))
        # self.__fid.write('%s"died": "%s",\n'% (white_space, ""))
        # self.__fid.write('%s"gramps_id": "%s",\n'% (white_space, id))
        if len(p.parent_id) > 0:
            self.__fid.write('%s"children": [\n' % white_space)
            i = 0
            for pid in p.parent_id:
                self.__write_json_for_fan_chart_ancestors(pid, level + 1)
                if i == 0:
                    self.__fid.write('%s,\n' % white_space2)
                i = i + 1
            self.__fid.write("%s]\n" % white_space)
        self.__fid.write("%s}\n" % white_space2)

    def __write_json_for_fan_chart_descendants(self, id, level):
        p = self.all_persons[id]
        white_space = '   ' * level
        white_space2 = '   ' * (level - 1)
        self.__fid.write('%s{\n' % white_space2)
        self.__fid.write('%s"name": "%s",\n' % (white_space, p.shortest_name))
        # self.__fid.write('%s"generation": "%d",\n'% (white_space, level))
        # self.__fid.write('%s"gender": "%s",\n'% (white_space, p.gender))
        self.__fid.write('%s"color": "%s",\n' % (white_space, p.color))
        self.__fid.write('%s"href": "%s",\n' % (white_space, p.link))
        # if p.birth_date == False:
        # self.__fid.write('%s"born": "",\n' % (white_space))
        # else:
        # self.__fid.write('%s"born": "%s",\n'% (white_space, '{0.year:4d}'.format(p.birth_date)))
        # self.__fid.write('%s"died": "%s",\n'% (white_space, ""))
        # self.__fid.write('%s"gramps_id": "%s",\n'% (white_space, id))
        list_of_cid = []
        for index, family in enumerate(p.family):
            if len(family.child_id) > 0:
                for cid in family.child_id:
                    list_of_cid.append(cid)
        if len(list_of_cid) > 0:
            self.__fid.write('%s"children": [\n' % white_space)
            i = 0
            for cid in list_of_cid:
                self.__write_json_for_fan_chart_descendants(cid, level + 1)
                if i != (len(list_of_cid) - 1):
                    self.__fid.write('%s,\n' % white_space2)
                i = i + 1
            self.__fid.write("%s]\n" % white_space)
        self.__fid.write("%s}\n" % white_space2)

    # def write_fan_chart_ancestors(self):
    #    self.__fid.write("<h3>Ancestors</h3>\n")
    #    self.__fid.write("<div id='fanchart_ancestors'></div>\n")
    #    self.__fid.write("<script>\n")
    #    self.__fid.write("var json_ancestors = ")
    #    self.__write_json_for_fan_chart_ancestors(self.person.id, 1)
    #    self.__fid.write(";\n")
    #    self.__fid.write("drawFanChart(json_ancestors, 1);\n")
    #    self.__fid.write("</script>\n")

    def write_fan_chart_descendants(self):
        self.__fid.write("<h3>Descendants</h3>\n")
        self.__fid.write("<div id='fanchart_descendants'></div>\n")
        self.__fid.write("<script>\n")
        self.__fid.write("var json_descendants = ")
        self.__write_json_for_fan_chart_descendants(self.person.id, 1)
        self.__fid.write(";\n")
        self.__fid.write("drawFanChart(json_descendants, 0);\n")
        self.__fid.write("</script>\n")

    def write_chart_navigator(self):
        self.__fid.write("<h3>Navigator</h3>\n")
        self.__fid.write("<div id='chart_navigator'></div>\n")
        self.__fid.write("<script>\n")
        self.__fid.write('var jsonNavigator = {\n   "nodes": [\n')
        for id, p in self.all_persons.items():
            # print p.color
            self.__fid.write('      {"id": "%s", "birth_year":"%s", "url":"%s", "color": "%s"},\n' % (
                p.id, p.birth_year, p.link, p.color))
        self.__fid.write('   ],\n   "links":[\n')
        for id, p in self.all_persons.items():
            for parent_id in p.parent_id:
                self.__fid.write('      {"source": "%s", "target": "%s", "type": "parent"},\n' % (p.id, parent_id))
            for index, family in enumerate(self.all_persons[id].family):
                if len(family.spouse_id) > 0:
                    self.__fid.write(
                        '      {"source": "%s", "target": "%s", "type": "spouse"},\n' % (p.id, family.spouse_id))
        self.__fid.write("   ]\n};\n")
        self.__fid.write("drawChartNavigator(jsonNavigator);\n")
        self.__fid.write("</script>\n")


class Gedcom2html:
    class Options:
        def __init__(self):
            self.input_file = ""
            self.output_path = "HTML"
            self.sc_project = ""
            self.sc_security = ""
            self.title = "gedcom2html by picnic projects"
            self.home_person_id = ""

    def __init__(self):
        self.options = self.Options()

    def __copy_assets(self, gedcom_file):
        try:
            shutil.rmtree('HTML')
        except:
            pass
        path, fname = os.path.split(gedcom_file)
        os.makedirs('HTML/js')
        os.makedirs('HTML/css')
        shutil.copy2(gedcom_file, 'HTML/' + fname)
        shutil.copy2('gedcom2html.css', 'HTML/css/')
        shutil.copy2('gedcom2html.v4.js', 'HTML/js/')
        shutil.copy2('assets/css/font-awesome.min.css', 'HTML/css/')
        shutil.copy2('assets/css/bootstrap.min.css', 'HTML/css/')
        shutil.copy2('assets/js/d3.v4.min.js', 'HTML/js/')
        shutil.copy2('assets/js/bootstrap.min.js', 'HTML/js/')
        shutil.copy2('assets/js/jquery-3.1.1.min.js', 'HTML/js/')
        shutil.copytree('assets/font-awesome/fonts', 'HTML/fonts/')

    def __create_strings(self, p):
        # shortest_name
        if len(p.nick_name) > 0:
            p.shortest_name = p.nick_name
        else:
            p.shortest_name = p.first_name.split(' ')[0]

        # short_name
        p.short_name = f"{p.surname} {p.shortest_name} "

        # string_short
        if p.gender == 'M':
            s = "<i class='fa fa-mars'></i>"
        else:
            s = "<i class='fa fa-venus'></i>"
        p.string_short = f"{s} {p.short_name} "

        # string_dates
        s = ""
        p.birth_year = ""
        if p.birth_date != False:
            s = s + "<i class='fa fa-star'></i> %s " % '{0.day:02d}-{0.month:02d}-{0.year:4d}'.format(p.birth_date)
            p.birth_year = '{0.year:4d}'.format(p.birth_date)
        if p.death_date != False:
            s = s + "<i class='fa fa-plus'></i> %s " % '{0.day:02d}-{0.month:02d}-{0.year:4d}'.format(p.death_date)
        if p.birth_date != False and p.death_date != False:
            # self.death_date.year - self.birth_date.year - ((today.month, today.day) < (born.month, born.day))
            age = p.death_date.year - p.birth_date.year
            if age == 0:
                age = p.death_date.month - p.birth_date.month
                s = s + "(%s months) " % age
            else:
                s = s + "(%s years) " % age
        p.string_dates = s

        # link
        s = "%s_%s.html" % (p.id, p.shortest_name)
        s = s.replace(' ', '_')
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        p.link = ''.join(c for c in s if c in valid_chars)

        # string_long
        if len(p.string_dates) > 0:
            p.string_long = (
                    "<a href='%s'>%s</a> <span class='dates'>%s</span>" % (p.link, p.string_short, p.string_dates))
        else:
            p.string_long = ("<a href='%s'>%s</a>" % (p.link, p.string_short))

    def __write_index_html(self, link):
        fid = open('HTML/index.html', 'w')
        fid.write('<meta http-equiv="refresh" content="0; url=%s">' % link)
        fid.close

    def write_html(self):
        self.__copy_assets(self.options.file_path)
        g = GedcomParser(self.options.file_path)
        all_persons = g.get_persons()
        id_list = list(all_persons.keys())
        id_list.sort()
        for id in id_list:
            self.__create_strings(all_persons[id])
        if len(self.options.home_person_id) > 0:
            self.__write_index_html(all_persons[self.options.home_person_id].link)
        else:
            self.__write_index_html(all_persons[id_list[0]].link)
        for id in id_list:
            p = all_persons[id]
            h = Html(g, p, all_persons, self.options)
        # p = all_persons[id_list[1]]
        # h = Html(p, all_persons, self.options)
