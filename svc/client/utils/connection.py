from pydantic import BaseModel


class Connection(BaseModel):
    '''
        This class represents connection to the
    backend service.
    '''
    host: str
    port: str

    def build_url(self) -> str:
        return 'http://' + ':'.join([self.host, self.port])