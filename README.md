# StudioSync-API

### Expected endpoints

#### Pipe Out -> Provider
  - `POST v1/project` + body `{ ... }`, => 201 + row_id, 400 
  - `POST v1/version-change` + body `{ ... }`, => 201 + row_id, 400
  - `POST v1/file` + body `{ ... }`, => 201 + row_id, 400
  - `PUT v1/project` + body `{ ... }`, => 200 + row_id, 400 

#### Provider -> Client
  - `GET v1/version-change` + query string (optional) `start_id=(1)&limit=20000&skip=0&project_name=ex1&sort_by=id&sort_order=ASC`
  - `GET v1/file-updates`
#### Client -> Pipe In
  - `GET v1/version-change` + query string (optional) `start_id=(1)&datetime_min=0&datetime_max=max(int)&limit=20000&skip=0&project_name=ex1&sort_by=id&sort_order=ASC` + entity_type,entity_name,task
#### Client <- Pipe In
  - `PUT v1/version-change/{id}/processed` + body `{"processed": true}`
  - `POST v1/origin` + body `{ ... }`, => 201 + row_id, 400
  - `POST v1/project` + body `{ ... }`, => 201 + row_id, 400

