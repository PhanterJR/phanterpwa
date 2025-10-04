import os
from datetime import datetime
from pydal import Field
from pydal.validators import (
    IS_IN_DB,
    IS_EMPTY_OR,
    IS_DATETIME
)


class pyDALTables():
    def __init__(self, db):
        self.db = db
        self.db.define_table('phanterpwagallery',
            Field('folder'),
            Field('filename'),
            Field('alias_name'),
            Field('content_type')
        )

        self.db.define_table('auth_user_phanterpwagallery',
            Field('phanterpwagallery', 'reference phanterpwagallery'),
            Field('auth_user', 'reference auth_user', requires=IS_EMPTY_OR(IS_IN_DB(self.db, self.db.auth_user))),
            Field('subfolder'),
            Field('last_update', 'datetime', default=datetime.now(), requires=IS_EMPTY_OR(IS_DATETIME()))
        )


class PhanterpwaGalleryUserImage():

    def __init__(self, id_user, db, projectConfig, appname="api"):
        self.db = db
        self.id_user = id_user
        self.upload_folder = os.path.normpath(
            os.path.join(projectConfig["PROJECT"]["path"], "backapps", appname, "uploads")
        )
        self.projectConfig = projectConfig

    @property
    def id_image(self):
        q_image = self.db(
            (self.db.auth_user_phanterpwagallery.auth_user == self.id_user) &
            (self.db.auth_user_phanterpwagallery.subfolder == 'profile') &
            (self.db.auth_user_phanterpwagallery.phanterpwagallery == self.db.phanterpwagallery.id)).select(
                self.db.auth_user_phanterpwagallery.id).last()
        if q_image:
            return q_image.id

    def alias_name(self, filename, id_image):
        ext = ""
        f_name = filename
        if "." in filename:
            ext = filename.split(".")[-1]
        f_name = "{0}.{1}".format(id_image, ext)
        return f_name

    def set_image(self, filename, file, content_type):
        db = self.db
        target_folder = os.path.join(self.upload_folder, "user_%s" % self.id_user, 'profile')
        os.makedirs(target_folder, exist_ok=True)
        q_image = self.db(
            (self.db.auth_user_phanterpwagallery.auth_user == self.id_user) &
            (self.db.auth_user_phanterpwagallery.subfolder == 'profile')).select(
                self.db.auth_user_phanterpwagallery.phanterpwagallery)
        if q_image:
            for q in q_image:
                t = os.path.join(os.path.join(target_folder, q.phanterpwagallery.alias_name))
                if os.path.exists(t):
                    try:
                        os.remove(t)
                    except OSError as e:
                        print("Error try delete {0}. Error: {1}".format(t, e))
                    else:
                        self.db(
                            self.db.phanterpwagallery.id == q.phanterpwagallery.id).delete()
            self.db.commit()
        id_new_image = self.db.phanterpwagallery.insert(
            folder=os.path.join("user_%s" % self.id_user, 'profile'),
            filename=filename,
            content_type=content_type)
        if id_new_image:
            alias_name = self.alias_name(filename, id_new_image)
            db.phanterpwagallery[id_new_image].update_record(alias_name=alias_name)

            with open(
                    os.path.join(target_folder, alias_name),
                    'wb') as new_image:
                new_image.write(file)
            new_vinculo = db.auth_user_phanterpwagallery.insert(
                phanterpwagallery=id_new_image,
                auth_user=self.id_user,
                subfolder="profile")
            if new_vinculo:
                self.db.commit()
                return new_vinculo

    @property
    def path_image(self):
        q_image = self.db(
            (self.db.auth_user_phanterpwagallery.auth_user == self.id_user) &
            (self.db.auth_user_phanterpwagallery.subfolder == 'profile') &
            (self.db.auth_user_phanterpwagallery.phanterpwagallery)).select(
                self.db.auth_user_phanterpwagallery.phanterpwagallery).last()
        if q_image:
            file = os.path.normpath(os.path.join(
                q_image.phanterpwagallery.folder,
                q_image.phanterpwagallery.alias_name
            ))
            if os.path.exists(file):
                return file


class PhanterpwaGalleryUpload(object):
    def __init__(self, db, _id=None):
        super(PhanterpwaGalleryUpload, self).__init__()
        self.db = db
        self.id = _id

    def insert_or_update(self, file, folder, filename, content_type):
        os.makedirs(folder, exist_ok=True)
        q_image = self.db(self.db.phanterpwagallery.id == self.id).select().first()
        if q_image:
            try:
                os.remove(os.path.join(folder, "{}".format(q_image.alias_name)))
            except OSError:
                pass
            new_alias_name = self.alias_name(filename, self.id)
            q_image.update_record(
                folder=folder,
                filename=filename,
                content_type=content_type,
                alias_name=new_alias_name
            )

            with open(os.path.join(folder, "{}".format(new_alias_name)), 'wb') as new_image:
                new_image.write(file)
            self.db.commit()
        else:
            id_image = self.db.phanterpwagallery.insert(
                folder=folder,
                filename=filename,
                content_type=content_type)
            if id_image:
                new_alias_name = self.alias_name(filename, id_image)
                self.db(self.db.phanterpwagallery.id == id_image).update(alias_name=new_alias_name)
                self.db.commit()
                self.id = id_image
                with open(
                        os.path.join(folder, "{}".format(new_alias_name)),
                        'wb') as new_image:
                    new_image.write(file)
        return self.id

    def alias_name(self, filename, id_image):
        ext = ""
        f_name = filename
        if "." in filename:
            ext = filename.split(".")[-1]
        f_name = "{0}.{1}".format(id_image, ext)
        return f_name

    def delete(self):
        q_image = self.db(self.db.phanterpwagallery.id == self.id).select().first()
        if q_image:
            try:
                os.remove(os.path.join(q_image.folder, "%s.%s" % (q_image.id, q_image.extensao)))
            except OSError:
                pass
            q_image.delete_record()
            self.db.commit()


class PhanterpwaGalleryImage():

    def __init__(self, sub_folder, db, projectConfig, id_image=0, appname="api"):
        self.db = db
        self.upload_folder = os.path.normpath(
            os.path.join(projectConfig["PROJECT"]["path"], "backapps", appname, "uploads")
        )
        self.projectConfig = projectConfig
        self.sub_folder = sub_folder
        self.id_image = id_image

    def alias_name(self, filename, id_image):
        ext = ""
        f_name = filename
        if "." in filename:
            ext = filename.split(".")[-1]
        f_name = "{0}.{1}".format(id_image, ext)
        return f_name

    def set_image(self, filename, file, content_type):
        db = self.db
        target_folder = os.path.join(self.upload_folder, self.sub_folder)
        os.makedirs(target_folder, exist_ok=True)
        rel_folder = os.path.join(self.sub_folder)
        if self.id_image:
            q_image = self.db(
                (self.db.phanterpwagallery.id == self.id_image)).select().first()
            if q_image:
                id_new_image = q_image.update_record(
                    folder=rel_folder,
                    filename=filename,
                    content_type=content_type
                )

            else:
                id_new_image = self.db.phanterpwagallery.insert(
                    folder=rel_folder,
                    filename=filename,
                    content_type=content_type
                )

        else:
            id_new_image = self.db.phanterpwagallery.insert(
                folder=rel_folder,
                filename=filename,
                content_type=content_type
            )

        self.db.commit()

        if id_new_image:
            self.id_image = id_new_image.id
            alias_name = self.alias_name(filename, self.id_image)
            q_img = db(db.phanterpwagallery.id == self.id_image).select().first()
            q_img.update_record(
                alias_name=alias_name
            )
            self.db.commit()
            with open(
                    os.path.join(target_folder, alias_name),
                    'wb') as new_image:
                new_image.write(file)
            return self.id_image

    @property
    def path_image(self):
        q_image = self.db(
            (self.db.phanterpwagallery.id == self.id_image)).select().last()
        if q_image:
            file = os.path.normpath(os.path.join(
                self.upload_folder,
                q_image.folder,
                q_image.alias_name
            ))
            if os.path.exists(file):
                return file


class PhanterpwaGalleryFile():

    def __init__(self, sub_folder, db, projectConfig, id_file=0, appname="api"):
        self.db = db
        self.upload_folder = os.path.normpath(
            os.path.join(projectConfig["PROJECT"]["path"], "backapps", appname, "uploads")
        )
        self.projectConfig = projectConfig
        self.sub_folder = sub_folder
        self.id_file = id_file

    def alias_name(self, filename, id_file):
        ext = ""
        f_name = filename
        if "." in filename:
            ext = filename.split(".")[-1]
        f_name = "{0}.{1}".format(id_file, ext)
        return f_name

    def set_file(self, filename, file, content_type):
        db = self.db
        target_folder = os.path.join(self.upload_folder, self.sub_folder)
        os.makedirs(target_folder, exist_ok=True)
        rel_folder = os.path.join(self.sub_folder)
        if self.id_file:
            s_file = self.db(
                (self.db.phanterpwagallery.id == self.id_file)).select().first()
            if s_file:
                id_new_file = s_file.update_record(
                    folder=rel_folder,
                    filename=filename,
                    content_type=content_type
                )

            else:
                id_new_file = self.db.phanterpwagallery.insert(
                    folder=rel_folder,
                    filename=filename,
                    content_type=content_type
                )

        else:
            id_new_file = self.db.phanterpwagallery.insert(
                folder=rel_folder,
                filename=filename,
                content_type=content_type
            )

        self.db.commit()

        if id_new_file:
            self.id_file = id_new_file.id
            alias_name = self.alias_name(filename, self.id_file)
            q_img = db(db.phanterpwagallery.id == self.id_file).select().first()
            q_img.update_record(
                alias_name=alias_name
            )
            self.db.commit()
            with open(
                    os.path.join(target_folder, alias_name),
                    'wb') as new_file:
                new_file.write(file)
            return self.id_file

    @property
    def path_file(self):
        s_file = self.db(
            (self.db.phanterpwagallery.id == self.id_file)).select().last()
        if s_file:
            file = os.path.normpath(os.path.join(
                self.upload_folder,
                s_file.folder,
                s_file.alias_name
            ))
            if os.path.exists(file):
                return file
