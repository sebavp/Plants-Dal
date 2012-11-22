# -*- coding: utf-8 -*


class Plant(object):
    def __init__(self, plant=None):
        if plant:
            self.name = plant.get('name')
            self.photo = plant.get('photo')
            self.wiki = plant.get('wiki')
            self.descriptors = plant.get('descriptors')
            self.distance = plant.get('distance',0)

    def save(self, db):
        db.execute("INSERT INTO leaves(name,photo,wiki, descriptors) values (%(name)s,%(photo)s,%(wiki)s,%(descriptors)s);",
        {'name':self.name,'photo':self.photo,'wiki':self.wiki,'descriptors':self.descriptors})

    @staticmethod
    def _db_to_plant(plant_result):
        if plant_result:
            plant = {'mame':plant_result[0],'photo':plant_result[1],'wiki':plant_result[2],'descriptors':plant_result[3]}
            if len(plant_result)>4:
                plant['distance'] = plant_result[4]
            return plant
            # return Plant(plant)
        return None

    @staticmethod
    def retrieve(db, name):
        db.execute("SELECT name,photo,wiki,descriptors FROM Leaves WHERE name=%s LIMIT 1",(name,))
        plant = db.fetchone()
        if plant:
            return Plant._db_to_plant(plant)
        return None


    @staticmethod
    def search(db, descriptors):
        db.execute('''SELECT name, photo, wiki, descriptors, vdistance(descriptors ,cast(%s as double precision[])) as distance
                      FROM Leaves
                      ORDER BY distance ASC
                      LIMIT 1''', (descriptors,))
        return Plant._db_to_plant(db.fetchone())