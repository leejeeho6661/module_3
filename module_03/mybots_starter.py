from scrapy.crawler import CrawlerProcess
# 프로세스에서 여러 개의 스크래피 크롤러를 동시에 실행하는 클래스이다.
# 자동실행하는 모듈이다.
from scrapy.utils.project import get_project_settings
# CrawlerProcess로 전달하는 스파이더를 자동으로 가져오고 get_project_settings를 사용하여 프로젝트 설정과 함께 설정 인스턴스를 가져올 수 있다.
from apscheduler.schedulers.twisted import TwistedScheduler
# 
# 스케쥴러 객체 불러옴 https://apscheduler.readthedocs.io/en/stable/modules/schedulers/twisted.html
from module_03.spiders.mybots import MybotsSpider
# 스파이더 불러옴




process = CrawlerProcess(get_project_settings())
# CrawlerProcess 개체는 Settings 개체로 인스턴스화해야 한다. -> 이후 crawlerprocess사용가능 
# https://docs.scrapy.org/en/latest/topics/practices.html?highlight=get_project_settings()#run-scrapy-from-a-script
scheduler = TwistedScheduler()
# 스케쥴러를 인스턴스화 -> 스케쥴러의 기능들을 사용할 수 있다. 
scheduler.add_job(process.crawl, 'interval', args=[MybotsSpider], seconds=10)
# 필요한 스케쥴러의 기능을 활성화, 10초,interval?,
scheduler.start()
# 스케쥴러 시작.
process.start(False)
# process.start() # the script will block here until all crawling jobs are finished -> 모든 크롤링작이 끝날때 까지 스크립트는 여기서 막힐 것이다. false처리해서 계속 돌게 하는거

#파이프라인을 다 만들고 mybots.py에 custom_setting 값을 입력해주고 
# scrapy crawl mybots -s JOBDRI= 을 입력
# crawl_mybot1폴더가 만들어짐
# mybots_starter.py 를 만들고 위의 내용 입력 
# python mybots_starter.py를 실행한다(cmd)