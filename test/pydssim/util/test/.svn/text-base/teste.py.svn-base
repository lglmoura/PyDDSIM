'''
Created on 28/08/2009

@author: LGustavo
'''

class StrategyExample :

    def __init__(self, func=None) :
        if func :
             self.execute = func

    def execute(self) :
        print "Oiginal execution"
        mapping = {}
        mapping["reference"] = ["resources", "tools", "programming", "webdesign", "tutorial", "research", "design", "tips", "web", "tutorials", "howto"]
        mapping["tutorial"] = ["photoshop", "webdesign", "tutorials", "programming", "howto", "tips", "reference", "web", "design", "photography", "css"]
        mapping["art"] = ["design", "inspiration", "illustration", "photography", "blog", "portfolio", "artist", "gallery", "graphics", "painting", "culture"]
        mapping["web"] = ["webdesign", "tools", "web2.0", "design", "webdev", "software", "tutorial", "css", "tutorials", "tool", "resources"]
        return mapping


def executeReplacement1() :
        print "Strategy 1"
        mapping = {}
        mapping["design"] = ["inspiration", "webdesign", "web", "blog", "art", "portfolio", "illustration", "typography", "photoshop", "graphic", "graphics"]
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
        return mapping


def executeReplacement2() :
        print "Strategy 2"
        mapping = {}
        mapping["design"] = ["inspiration", "webdesign", "web", "blog", "art", "portfolio", "illustration", "typography", "photoshop", "graphic", "graphics"]
        mapping["blog"] = ["design", "inspiration", "music", "art", "web2.0", "webdesign", "blogs", "photography", "wordpress", "web", "news"]
        mapping["video"] = ["youtube", "software", "tv", "music", "tools", "web2.0", "streaming", "tutorial", "videos", "media", "funny"]
        mapping["software"] = ["tools", "windows", "mac", "opensource", "freeware", "osx", "free", "programming", "linux", "web", "web2.0"]
        mapping["tools"] = ["web2.0", "software", "web", "webdesign", "twitter", "windows", "tool", "utilities", "resources", "reference", "online"]
        mapping["music"] = ["mp3", "blog", "download", "audio", "video", "guitar", "software", "free", "web2.0", "youtube", "radio"]
        mapping["programming"] = ["development", "tutorial", "software", "python", "reference", "java", "php", "web", "opensource", "javascript", "webdev"]
        mapping["webdesign"] = ["design", "web", "inspiration", "css", "webdev", "resources", "tutorials", "tutorial", "tools", "web2.0", "photoshop"]
        mapping["howto"] = ["tutorial", "tips", "linux", "reference", "tutorials", "diy", "photography", "ubuntu", "photoshop", "programming", "software"]
        return mapping

if __name__ == "__main__" :

    strat0 = StrategyExample()
    op = [executeReplacement1,executeReplacement2]
    
    strat1 = StrategyExample(op[0])
    strat2 = StrategyExample(op[1])

    map1 = strat0.execute()
    map2 = strat1.execute()
    map3 = strat2.execute()
    
    print "map1 ",len(map1.keys()) 
    print "map2 ",len(map2.keys()) 
    print "map3 ",len(map3.keys())  
