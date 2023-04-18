from django.utils import timezone


class BaseENT(object):

    def __init__(self,
                 id=None,
                 name=None,
                 status=1,
                 insert_logged_user_id=None,
                 update_logged_user_id=None,
                 transitionHistory_id=None,
                 transition_id=None,
                 transition=None,
                 datetime_created=None,
                 datetime_updated=None,
                 # uuid=None
                 ):
        self._id = id
        self._name = name
        self._status = status
        self._label = self._name
        self._insert_logged_user_id = insert_logged_user_id
        self._update_logged_user_id = update_logged_user_id
        self._insert_date = timezone.now()
        self._update_date = timezone.now()
        self._transitionHistory_id = transitionHistory_id
        self._transition_id = transition_id
        self._transition = transition
        self._datetime_created = datetime_created
        self._datetime_updated = datetime_updated
        # self._uuid = uuid

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def insert_logged_user_id(self):
        return self._insert_logged_user_id

    @insert_logged_user_id.setter
    def insert_logged_user_id(self, value):
        self._insert_logged_user_id = value

    @property
    def update_logged_user_id(self):
        return self._update_logged_user_id

    @update_logged_user_id.setter
    def update_logged_user_id(self, value):
        self._update_logged_user_id = value

    @property
    def insert_date(self):
        return self._insert_date

    @insert_date.setter
    def insert_date(self, value):
        self._insert_date = value

    @property
    def update_date(self):
        return self._update_date

    @update_date.setter
    def update_date(self, value):
        self._update_date = value

    @property
    def transition_id(self):
        return self._transition_id

    @transition_id.setter
    def transition_id(self, value):
        self._transition_id = value

    @property
    def transition(self):
        return self._transition

    @transition.setter
    def transition(self, value):
        self._transition = value

    @property
    def transitionHistory_id(self):
        return self._transitionHistory_id

    @transitionHistory_id.setter
    def transitionHistory_id(self, value):
        self._transitionHistory_id = value

    @property
    def datetime_created(self):
        return self._datetime_created

    @datetime_created.setter
    def datetime_created(self, value):
        self._datetime_created = value

    @property
    def datetime_updated(self):
        return self._datetime_updated

    @datetime_updated.setter
    def datetime_updated(self, value):
        self._datetime_updated = value

    # @property
    # def uuid(self):
    #     return self._uuid
    #
    # @uuid.setter
    # def uuid(self, value):
    #     self._uuid = values

    # def __eq__(self, other):
    #     return self.id == other.id and self.name == other.name

    # def __ne__(self, other):
    #     return not self == other
