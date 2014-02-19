'''
Created on 29/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''

 
class ServiceMap(object):
    def Map(self, resource):
        #print "****** Service *******"
        mapping = {}
        '''mapping["design"] = ["inspiration", "webdesign", "web", "blog", "art", "portfolio", "illustration", "typography", "photoshop", "graphic", "graphics"]
        mapping["blog"] = ["design", "inspiration", "music", "art", "web2.0", "webdesign", "blogs", "photography", "wordpress", "web", "news"]
        mapping["video"] = ["youtube", "software", "tv", "music", "tools", "web2.0", "streaming", "tutorial", "videos", "media", "funny"]
        mapping["software"] = ["tools", "windows", "mac", "opensource", "freeware", "osx", "free", "programming", "linux", "web", "web2.0"]
        mapping["tools"] = ["web2.0", "software", "web", "webdesign", "twitter", "windows", "tool", "utilities", "resources", "reference", "online"]
        mapping["music"] = ["mp3", "blog", "download", "audio", "video", "guitar", "software", "free", "web2.0", "youtube", "radio"]
        mapping["programming"] = ["development", "tutorial", "software", "python", "reference", "java", "php", "web", "opensource", "javascript", "webdev"]
        mapping["webdesign"] = ["design", "web", "inspiration", "css", "webdev", "resources", "tutorials", "tutorial", "tools", "web2.0", "photoshop"]
        mapping["reference"] = ["resources", "tools", "programming", "webdesign", "tutorial", "research", "design", "tips", "web", "tutorials", "howto"]
        mapping["tutorial"] = ["photoshop", "webdesign", "tutorials", "programming", "howto", "tips", "reference", "web", "design", "photography", "css"]
        mapping["art"] = ["design", "inspiration", "illustration", "photography", "blog", "portfolio", "artist", "gallery", "graphics", "painting", "culture"]
        mapping["web"] = ["webdesign", "tools", "web2.0", "design", "webdev", "software", "tutorial", "css", "tutorials", "tool", "resources"]
        mapping["howto"] = ["tutorial", "tips", "linux", "reference", "tutorials", "diy", "photography", "ubuntu", "photoshop", "programming", "software"]
        ''' 
        mapping["teste"] = ["teste"]
        mapping["teste1"] = ["teste1"]
        return mapping

class HardwareMap(object):
    def Map(self, resource):
        #print "****** Hardware *********"
        
        mapping = {}
        '''mapping["io"] = ["hd", "dvd", "cdrom", "flash", "floppy"]
        mapping["process"] = ["Clic", "Time"]
        mapping["print"] = ["hp", "laser", "jato"]
        mapping["memory"] = ["memory","DDR"]
        '''
        mapping["memory"] = ["memory"]
        mapping["memory1"] = ["memory1"]
        
        return mapping

 
class ResourceMap(object):
    '''
    classdocs
    '''

    def __init__(self, resourceBehavior):
        '''
        Constructor
        '''
        
        self.resourceBehavior = resourceBehavior

    def Map(self):
        return self.resourceBehavior.Map(self)