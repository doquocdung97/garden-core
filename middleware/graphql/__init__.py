from ariadne import QueryType, make_executable_schema,snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel
from .gql_schema_generator import generate_gql_schema_str
class User(BaseModel):
    name: str
    id: UUID

class HelloMessage(BaseModel):
    body: str
    user: UUID
    testdata:User


query = QueryType()


@query.field('hello')
def resolve_hello(_, info) -> HelloMessage:
    request = info.context['request']
    user_agent = request.headers.get('user-agent', 'guest')
    return HelloMessage(
        body='Hello, %s!' % user_agent,
        from_user=uuid4(),
    )


# Generate type_defs from Pydantic types in query definition.
type_defs = generate_gql_schema_str([query])

schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers,
)
app = GraphQL(schema, debug=True)