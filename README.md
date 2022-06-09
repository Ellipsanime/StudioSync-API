# StudioSync-API

### Expected endpoints

#### Pipe Out -> Provider
  - `POST v1/project` + body `{ ... }`, => 201 + new_id, 400 
  - `POST v1/version-change` + body `{ ... }`, => 201 + new_id, 400
  - `POST v1/file` + body `{ ... }`, => 201 + new_id, 400
#### Provider -> Client
  - `GET v1/version-change` + query string (optional) `datetime_min=0&datetime_max=max(int)&limit=500&skip=0&project_name=ex1&sort_by=id&sort_order=ASC`
#### Client -> Pipe In
  - `GET v1/version-change` + query string (optional) `datetime_min=0&datetime_max=max(int)&limit=500&skip=0&project_name=ex1&sort_by=id&sort_order=ASC`
#### Client <- Pipe In
  - `PUT v1/version-change/{id}/processed` + body `{"processed": true}`
  - `POST v1/origin` + body `{ ... }`, => 201 + new_id, 400
  - `POST v1/project` + body `{ ... }`, => 201 + new_id, 400

