#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-3-2 下午2:09
# @Author  : Sugare
# @mail    : 30733705@qq.com
# @File    : orm.py
# @Software: PyCharm
import sys
import datetime
from peewee import *
from peewee import SelectQuery
import MySQLdb

#db = MySQLDatabase(host='localhost', user='root', passwd=123456, database='blog', charset='utf8', port=3306)
db = MySQLDatabase('noblog', user='root', password='123456', charset='utf8')

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

class noblog(BaseModel):
    author = CharField(verbose_name=u'作者', default='Sugare')
    title = CharField(verbose_name=u'标题')
    tags = CharField(verbose_name=u'标签', help_text=u'用逗号分隔')
    summary = TextField(verbose_name=u'摘要')
    content = TextField(verbose_name=u'正文')
    view_times = IntegerField(default=0)
    zan_times = IntegerField(default=0)
    created_date = DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))

    def get_tags(self):
        tags_list = self.tags.split(',')
        while '' in tags_list:
            tags_list.remove('')
        return tags_list

# class tags(BaseModel):
#     tag_choices = (
#         (1, 'linux'),
#         (2, 'docker'),
#         (3, 'python'),
#         (4, '数据库'),
#         (5, 'html'),
#         (6, '网络'),
#         (7, '云计算'),
#         (8, 'javascript'),
#         (9, 'bootstrap'),
#     )
#     blog = ForeignKeyField(noblog, on_delete='CASCADE')
#     tag = IntegerField(choices=tag_choices)
def indexTag():
    l = []
    sq = noblog.select()
    for i in sq.execute():
        for j in i.get_tags():
            if j not in l:
                l.append(j)
    return l

def rightbarDate():
    l = []
    sq = noblog.select(noblog.created_date, fn.Count(noblog.created_date).alias('count')).group_by(noblog.created_date)
    for i in sq.execute():
        # l.append(i)
        l.insert(0,i)
    return l

def rightbarHot():
    l = []
    sq = noblog.select().order_by(noblog.zan_times.desc()).paginate(0,5)
    for i in sq.execute():
        l.append(i)
    return l


def latest():
    data = (noblog.select(fn.MAX(noblog.id).alias('latest'))).get()
    return data.latest

def dateData(date):
    l = []
    sq = noblog.select().where(noblog.created_date=='{}'.format(date))
    for i in sq.execute():
        l.append(i)
    return l

def tagData(tag):
    l = []
    sq = noblog.select()
    for i in sq.execute():
        if tag in i.get_tags():
            l.append(i)
    return l


def PagerTotalItem():
    l = []
    data = (noblog.select(fn.Count('*').alias('count'))).get()
    return data.count

def PagerPerItem(page, perItem):
    l = []
    sq = noblog.select().order_by(noblog.id).paginate(page, perItem)
    for i in sq:
        l.append(i)
    return l


def getData(bid):
    try:
        data = noblog.get(noblog.id == bid)
    except:
        print('DoesNotExist the record')
        sys.exit(1)
    return data



html = '''
<h4 class="content-h4">一.docker介绍</h4>
<p>为充分满足企业客户在使用 DaoCloud Enterprise 平台过程中面对的多元化场景需求，DaoCloud Enterprise 平台为企业开发团队和第三方软件开发商提供了标准开放的平台模块接口 API，提供丰富的开发者文档和包括 Java、Python、JavaScript 等语言的 SDK 开发包，帮助开发团队和开发者快速开发并上线模块应用，帮助企业客户快速实现快速增长的业务功能需求。
    通过模块中心，DaoCloud 打造了更加开放的平台生态，使得企业开发团队和第三方开发者可以选择通过利用 DaoCloud Services 精益开发协作平台进行对接代码仓库、持续构建镜像、持续发布镜像的自动化精益开发流程，而且可以通过 DaoCloud 镜像市场来分享至更广阔的社区。
    <img class="img-responsive" styletag="margin: 0 auto" src="/static/img/info1.jpg" alt="">
</p>
<h4>二.docker安装</h4>
<p>
目前除了官方模块之外，多家合作厂商积极与 DaoCloud 一起开发平台功能模块，通过严格认证之后的模块就可上架到模块商店，供所有平台企业客户在其 IT 平台上进行安装部署并使用。联想硬件管理和监控模块是经过联想和 DaoCloud 双方研发团队共同努力开发的认证模块，为使用联想服务器的平台客户提供更便捷的服务需求。
</p>
<h4>三.docker部署</h4>
<p>
通过模块中心，DaoCloud Enterprise 应用云平台变得更加灵活和开放。
系统监控中心
</p>
<h4>四.docker总结</h4>
<p>
企业客户 IT 信息系统运维的场景中，及时灵活的系统告警机制对于企业系统监控是非常重要的。DaoCloud Enterprise 在 2.4 版本中全面升级了系统监控中心。现在，运维团队不仅可以通过平台收到系统告警消息提示，而且还可以灵活设置告警策略，根据告警种类和触发条件通过邮件方式通知相关运维人员。
</p>
'''
html1 = '''
东汉末年，宦官当权，生灵涂炭，民不聊生。灵帝中平元年，张角兄弟发动黄巾起义，官军闻风丧胆。为抵抗黄巾，幽州太守刘焉出榜招兵。榜文前，刘备、关羽、张飞三兄弟萍水相逢。三人都有为国效力之心，而且志趣相投，于是桃园结为异姓兄弟，投靠刘焉。从军后刘、关、张显示出非凡的才能，一败黄巾于涿郡，二败黄巾于青州。不久，又救出被张角打败的董卓，但董卓见刘备是白身，并不答谢。张飞大怒，要斩董卓，被刘备劝住。刘关张与朱儁、孙坚进攻黄巾，大胜。朱儁、孙坚皆受封赏，只有刘备被冷落。很久之后，刘备才被封为定州中山府安喜县尉。到任四月，督邮来县巡视，借机索要贿赂。因刘备不从而欲存心陷害，张飞得知后怒鞭督邮，三人被迫弃去职位，投了刘恢。不久参加平定鱼阳之战，刘备因立功被任平原令，开始拥有一支人马。[1]
中平六年，汉灵帝死，少帝继位，为外戚大将军何进所制。十常侍诱杀何进，袁绍等领兵诛杀宦官，西凉刺史董卓趁机进兵京师、驱逐袁绍、灭丁原收吕布、废少帝立献帝，专权朝野，并毒死刘辩。司徒王允借寿诞之引，召集满朝公卿商议，曹操自告奋勇前往行刺，为董卓发觉，危急中献上自王允处借来的七星宝刀而脱身。[1]
曹操逃至中牟县为当时县令陈宫所获。陈宫义释曹操，并弃官随之离去。途经曹操之亲戚吕伯奢家时，因误会而杀害吕伯奢一家，并说出“宁教我负天下人，休教天下人负我”之语。陈宫愤怒，独自离开。曹操只身前往陈留，散尽家资招蓦兵马，亲友皆来相投，亦有了一支人马。曹操更写信给袁绍，并会齐中原豪杰。[1]
三国演义剧照
三国演义剧照(14张)
曹操、袁术等十八路诸侯与吕布对峙于汜水关，董卓派出华雄斩去十八镇诸侯多位上将，关羽自告奋勇却因自身的地位而被众诸侯所叱，唯曹操赏识人才，斟热酒令出战。酒尚温，关羽已斩华雄而归。随后，吕布骑赤兔马亲出虎牢关，袁绍亦派八路诸侯迎敌。众诸侯难敌吕布之勇，危难时候张飞救下公孙瓒而与吕布交手。因吕布奇勇，关羽、刘备先后出战，三人合力杀败吕布，吕布败退虎牢关。八路诸侯乘胜出击大获全胜，曹操暗中犒赏刘、关、张。[1]

'''


if __name__ == '__main__':
    db.connect()
    # noblog.create(title='{}'.format('abc'), essay='{}'.format(MySQLdb.escape_string(html)))
    #print(indexTag())
    for i in range(10):
       noblog.create(title='{}'.format('docker技术基础'), created_date='2017-3-1',content='{}'.format(html1), summary='{}'.format('3月2日，全国政协十二届五次会议新闻发布会在北京人民大会堂举行。图为一名记者使用新式设备在现场采访报道。据了解，这套设备叫做“钢铁侠多信道直播云台”，首次将裸眼与VR（虚拟现实）直播应用到全国两会新闻报道中。'), tags='html,javascript')
    #db.create_tables([noblog, ])
    #sq = SelectQuery(noblog, fn.Count(noblog.created_date).alias('count'))
    #sq = noblog.select().order_by(noblog.id.desc()).paginate(0,1)
    ##for i in sq.execute()
    #print(i)
    # sq = noblog.select().order_by(noblog.id).paginate(2, 8)
    # for i in sq:
    #     print(i.id)
    #print(PagerPerItem(2, 8))

    db.close()
    #
    # (Colors
    #  .select(Colors.group)
    #  .where(Colors.color << ('red', 'orange'))
    #  .group_by(Colors.group)
    #  .having(fn.COUNT(Colors.id) == 2))