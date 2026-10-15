# Feature Organization Standards

## Mandatory File Structure

**Every new feature or endpoint must be implemented in its own dedicated files.**

Large `views.py` and `serializers.py` files are **not allowed**.

Instead, use feature-based modules.

Example:

```text
apps/
└── documents/
├── views/
│   ├── __init__.py
│   ├── create_document.py
│   ├── update_document.py
│   ├── delete_document.py
│   ├── list_documents.py
│   ├── retrieve_document.py
│   └── merge_documents.py
│
├── serializers/
│   ├── __init__.py
│   ├── create_document.py
│   ├── update_document.py
│   ├── merge_document.py
│   ├── document_list.py
│   └── document_detail.py
│
├── services/
├── selectors/
└── models.py
```

---

# One Responsibility Per File

Every file must contain **only one logical responsibility**.

### Views

One view class per file.

Good:

```text
views/
create_document.py
update_document.py
delete_document.py
```

Bad:

```text
views.py
```

containing:

* CreateAPIView
* UpdateAPIView
* DeleteAPIView
* ListAPIView
* RetrieveAPIView
* Custom Actions

---

### Serializers

One serializer per file.

Good:

```text
serializers/
create_document.py
update_document.py
list_document.py
detail_document.py
```

Bad:

```python
serializers.py

class CreateSerializer(...)
class UpdateSerializer(...)
class DetailSerializer(...)
class ListSerializer(...)
class MergeSerializer(...)
```

---

# File Naming Convention

Use descriptive snake_case names based on the feature or responsibility.

Examples:

```text
create_document.py
update_document.py
delete_document.py
list_documents.py
retrieve_document.py
approve_document.py
merge_documents.py
```

Avoid generic names such as:

```text
helpers.py
utils.py
misc.py
common.py
new.py
temp.py
```

---

# Package Exports

Each package must expose its public classes through `__init__.py`.

Example:

```python
from .create_document import CreateDocumentAPIView
from .update_document import UpdateDocumentAPIView
from .delete_document import DeleteDocumentAPIView
```

Likewise for serializers:

```python
from .create_document import CreateDocumentSerializer
from .update_document import UpdateDocumentSerializer
from .detail_document import DocumentDetailSerializer
```

This allows imports like:

```python
from apps.documents.views import CreateDocumentAPIView
from apps.documents.serializers import CreateDocumentSerializer
```

---

# Maximum Responsibility Rule

Each file should implement **only one feature or one endpoint**.

If additional responsibilities are introduced, create a new file instead of extending an existing one.

Examples:

```
Create User
→ create_user.py

Reset Password
→ reset_password.py

Approve Invoice
→ approve_invoice.py

Merge Documents
→ merge_documents.py
```

Never combine unrelated endpoints into the same file.

---

# AI Agent Enforcement

When implementing new functionality, the AI agent **must**:

1. Create a new file under the appropriate `views/` directory.
2. Create a new file under the appropriate `serializers/` directory if a serializer is required.
3. Place exactly one view class in each view file.
4. Place exactly one serializer class in each serializer file.
5. Update the corresponding `views/__init__.py` and `serializers/__init__.py` to export the new classes.
6. Never append new endpoints or serializers to existing feature files unless modifying that exact functionality.
7. Follow the existing Service → Selector → Database architecture without embedding business logic in views or serializers.

---

# Final Rule

**One file = One responsibility.**

Every endpoint should have:

* One dedicated view file.
* One dedicated serializer file (if applicable).
* Business logic in a service.
* Data access in a selector.

This structure is mandatory for all future development and helps maintain a clean, scalable, and conflict-free codebase.

---

# DRF View Standards

## Mandatory Rule

This codebase uses Class-Based Views only.

The AI agent must NEVER create:

* Function Based Views (FBV)
* @api_view decorated functions
* Mixed FBV/CBV implementations

Example of prohibited code:

```python
@api_view(["GET"])
def get_document(request):
...
```

```python
def create_document(request):
...
```

These patterns are not allowed.

---

# Universal API Response Standard

## Mandatory Response Structure

**ALL API endpoints must return responses in this exact format:**

### Success Response Format

```python
{
"success": true,
"message": "Operation completed successfully",
"data": {},  # or [] for list endpoints
"errors": null,
"status_code": 200,
"timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response Format

```python
{
"success": false,
"message": "A user-friendly error description",
"data": null,
"errors": {},  # Field-specific errors for validation failures
"status_code": 400,
"timestamp": "2024-01-15T10:30:00Z"
}
```

### Paginated Response Format

```python
{
"success": true,
"message": "Records retrieved successfully",
"data": [],  # Actual data array
"pagination": {
"count": 100,
"next": "http://api.example.com/items/?page=3",
"previous": "http://api.example.com/items/?page=1",
"page_size": 10,
"current_page": 2,
"total_pages": 10
},
"errors": null,
"status_code": 200,
"timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Response Wrapper Classes

### Base Response Structure

```python
# utils/response.py

from rest_framework.response import Response
from datetime import datetime
from typing import Any, Dict, Optional, List

class APIResponse:
"""Universal API Response Wrapper"""
@staticmethod
def success(
message: str = "Success",
data: Any = None,
status_code: int = 200
) -> Response:
return Response({
"success": True,
"message": message,
"data": data,
"errors": None,
"status_code": status_code,
"timestamp": datetime.utcnow().isoformat()
}, status=status_code)
@staticmethod
def created(
message: str = "Resource created successfully",
data: Any = None
) -> Response:
return APIResponse.success(message, data, 201)
@staticmethod
def error(
message: str = "An error occurred",
errors: Any = None,
status_code: int = 400
) -> Response:
return Response({
"success": False,
"message": message,
"data": None,
"errors": errors,
"status_code": status_code,
"timestamp": datetime.utcnow().isoformat()
}, status=status_code)
@staticmethod
def validation_error(
errors: Dict[str, List[str]],
message: str = "Validation failed"
) -> Response:
return APIResponse.error(message, errors, 400)
@staticmethod
def not_found(
message: str = "Resource not found"
) -> Response:
return APIResponse.error(message, None, 404)
@staticmethod
def unauthorized(
message: str = "Authentication required"
) -> Response:
return APIResponse.error(message, None, 401)
@staticmethod
def forbidden(
message: str = "Permission denied"
) -> Response:
return APIResponse.error(message, None, 403)
@staticmethod
def paginated(
data: List[Any],
pagination: Dict[str, Any],
message: str = "Records retrieved successfully"
) -> Response:
return Response({
"success": True,
"message": message,
"data": data,
"pagination": pagination,
"errors": None,
"status_code": 200,
"timestamp": datetime.utcnow().isoformat()
}, status=200)
```

---

## Custom Response Renderer

```python
# renderers.py

from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from datetime import datetime

class UniversalAPIJSONRenderer(JSONRenderer):
"""Ensures all responses follow the universal format"""
def render(self, data, accepted_media_type=None, renderer_context=None):
response = renderer_context.get('response') if renderer_context else None
# If response is already in our format, pass through
if data and isinstance(data, dict) and 'success' in data:
return super().render(data, accepted_media_type, renderer_context)
# Transform successful responses
if response and 200 <= response.status_code < 300:
formatted_data = {
"success": True,
"message": "Operation completed successfully",
"data": data,
"errors": None,
"status_code": response.status_code,
"timestamp": datetime.utcnow().isoformat()
}
return super().render(formatted_data, accepted_media_type, renderer_context)
# Transform error responses
return super().render(data, accepted_media_type, renderer_context)

def universal_exception_handler(exc, context):
"""Custom exception handler for universal response format"""
response = exception_handler(exc, context)
if response is not None:
return Response({
"success": False,
"message": str(exc.detail) if hasattr(exc, 'detail') else "An error occurred",
"data": None,
"errors": response.data,
"status_code": response.status_code,
"timestamp": datetime.utcnow().isoformat()
}, status=response.status_code)
return response
```

---

## View Implementation with Universal Responses

### ViewSet Example

```python
# views.py

from rest_framework.viewsets import ModelViewSet
from utils.response import APIResponse

class DocumentViewSet(ModelViewSet):
serializer_class = DocumentSerializer
queryset = Document.objects.all()
def list(self, request, *args, **kwargs):
queryset = self.filter_queryset(self.get_queryset())
page = self.paginate_queryset(queryset)
if page is not None:
serializer = self.get_serializer(page, many=True)
return APIResponse.paginated(
data=serializer.data,
pagination={
"count": self.paginator.page.paginator.count,
"next": self.paginator.get_next_link(),
"previous": self.paginator.get_previous_link(),
"page_size": self.paginator.page_size,
"current_page": self.paginator.page.number,
"total_pages": self.paginator.page.paginator.num_pages
},
message="Documents retrieved successfully"
)
serializer = self.get_serializer(queryset, many=True)
return APIResponse.success(
message="Documents retrieved successfully",
data=serializer.data
)
def create(self, request, *args, **kwargs):
serializer = self.get_serializer(data=request.data)
serializer.is_valid(raise_exception=True)
self.perform_create(serializer)
return APIResponse.created(
message="Document created successfully",
data=serializer.data
)
def retrieve(self, request, *args, **kwargs):
instance = self.get_object()
serializer = self.get_serializer(instance)
return APIResponse.success(
message="Document retrieved successfully",
data=serializer.data
)
def update(self, request, *args, **kwargs):
partial = kwargs.pop('partial', False)
instance = self.get_object()
serializer = self.get_serializer(instance, data=request.data, partial=partial)
serializer.is_valid(raise_exception=True)
self.perform_update(serializer)
return APIResponse.success(
message="Document updated successfully",
data=serializer.data
)
def destroy(self, request, *args, **kwargs):
instance = self.get_object()
self.perform_destroy(instance)
return APIResponse.success(
message="Document deleted successfully",
data=None
)
```

### APIView Example

```python
class MergeDocumentAPIView(APIView):
def post(self, request, *args, **kwargs):
try:
# Validate request
serializer = MergeDocumentSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
# Call service
result = DocumentService.merge_documents(
serializer.validated_data
)
return APIResponse.success(
message="Documents merged successfully",
data=result
)
except ValidationError as e:
return APIResponse.validation_error(
errors=e.message_dict,
message="Merge validation failed"
)
except PermissionError:
return APIResponse.forbidden(
message="You don't have permission to merge these documents"
)
except Exception as e:
return APIResponse.error(
message=str(e),
status_code=500
)
```

---

## Serializer Error Handling

```python
# serializers.py

from rest_framework import serializers
from utils.response import APIResponse

class DocumentSerializer(serializers.ModelSerializer):
class Meta:
model = Document
fields = '__all__'
def validate(self, data):
# Custom validation
if data.get('status') == 'published' and not data.get('content'):
raise serializers.ValidationError({
'content': 'Published documents must have content'
})
return data
```

---

# Message Standards

## Success Message Patterns

| Operation | Message Format |
|-----------|----------------|
| Create | "{Resource} created successfully" |
| Retrieve | "{Resource} retrieved successfully" |
| Update | "{Resource} updated successfully" |
| Delete | "{Resource} deleted successfully" |
| List | "{Resources} retrieved successfully" |
| Custom Action | "{Action} completed successfully" |

## Error Message Patterns

| Error Type | Message Format | HTTP Status |
|------------|----------------|--------------|
| Validation | "Validation failed" | 400 |
| Not Found | "{Resource} not found" | 404 |
| Unauthorized | "Authentication required" | 401 |
| Forbidden | "Permission denied" | 403 |
| Conflict | "{Resource} already exists" | 409 |
| Server Error | "Internal server error" | 500 |

---

**# View Selection Hierarchy

Mandatory ViewSet Rule

Every API endpoint must be implemented using a DRF ViewSet.

ViewSets are mandatory for all API endpoints, including:

CRUD operations

Read-only resources

Custom workflows

Bulk operations

Approval/rejection operations

Submission/transmission operations

Import/export operations

Any other API operation

The AI agent must NEVER create an API endpoint using:

APIView

GenericAPIView

ListAPIView

CreateAPIView

RetrieveAPIView

UpdateAPIView

DestroyAPIView

ListCreateAPIView

RetrieveUpdateAPIView

RetrieveDestroyAPIView

RetrieveUpdateDestroyAPIView

Function Based Views (FBV)

@api_view

Allowed ViewSet Types

The AI agent may use only the following DRF ViewSet patterns:

1. ModelViewSet

Use ModelViewSet when the resource supports normal CRUD operations.

from rest_framework.viewsets import ModelViewSet


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

2. ReadOnlyModelViewSet

Use ReadOnlyModelViewSet when the resource only supports:

List

Retrieve

from rest_framework.viewsets import ReadOnlyModelViewSet


class DocumentTemplateViewSet(ReadOnlyModelViewSet):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer

3. GenericViewSet + Mixins

Use GenericViewSet with the required mixins when the endpoint needs a limited subset of CRUD operations.

from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class DocumentViewSet(
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

This is still a ViewSet and is allowed.

Custom Operations

Custom operations MUST be implemented as ViewSet actions using @action.

Do not create a separate APIView for a custom operation.

Good:

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        document = self.get_object()

        result = DocumentService.approve(
            document=document,
            user=request.user,
        )

        return APIResponse.success(
            message="Document approved successfully",
            data=result,
        )

Bad:

class ApproveDocumentAPIView(APIView):
    def post(self, request, pk=None):
        ...

The APIView implementation is prohibited even when the operation is a complex workflow.

Collection Actions

For operations that act on a collection, use:

@action(
    detail=False,
    methods=["post"],
)
def bulk_import(self, request):
    ...

Example:

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=False, methods=["post"])
    def bulk_import(self, request):
        serializer = BulkImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = DocumentService.bulk_import(
            serializer.validated_data,
            request.user,
        )

        return APIResponse.success(
            message="Documents imported successfully",
            data=result,
        )

Detail Actions

For operations that act on one resource, use:

@action(
    detail=True,
    methods=["post"],
)
def approve(self, request, pk=None):
    ...

Example:

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        document = self.get_object()

        result = DocumentService.approve(
            document,
            request.user,
        )

        return APIResponse.success(
            message="Document approved successfully",
            data=result,
        )

Multiple HTTP Methods

A custom action may support multiple HTTP methods when required.

@action(
    detail=True,
    methods=["post", "delete"],
)
def archive(self, request, pk=None):
    ...

The selected methods must match the actual business requirement.

ViewSet Action Naming

Custom actions must use clear business-oriented names.

Good:

approve
reject
cancel
submit
transmit
merge
bulk_import
bulk_export
retry
restore
archive
publish
unpublish

Avoid generic names such as:

process
handle
execute
do_action
run
operation

unless the business domain specifically requires them.

Router Requirement

ViewSets must be registered through DRF routers whenever possible.

Preferred:

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    "documents",
    DocumentViewSet,
    basename="documents",
)

Custom actions are automatically exposed through the router.

For example:

@action(detail=True, methods=["post"])
def approve(self, request, pk=None):
    ...

produces an endpoint conceptually equivalent to:

POST /documents/{id}/approve/

Do not manually create URL mappings for standard CRUD ViewSet actions.

ViewSet Preference Order

The AI agent must select a ViewSet using the following order:

ModelViewSet

ReadOnlyModelViewSet

GenericViewSet + required mixins

There is no fourth or fifth fallback.

APIView and GenericAPIView are NOT fallback options.

No Exceptions Rule

Complexity does not justify using APIView.

The following are still required to use ViewSets:

Complex workflows

Multiple services

Multiple database operations

External API integrations

File uploads

File downloads

Bulk operations

Approval workflows

Submission workflows

Payment workflows

Import/export operations

Long-running operations

Custom request structures

Operations with no conventional CRUD equivalent

When an operation is not conventional CRUD, implement it as a ViewSet @action.

Example:

class SubmissionViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        serializer = SubmissionSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = SubmissionService.submit(
            submission=self.get_object(),
            data=serializer.validated_data,
            user=request.user,
        )

        return APIResponse.success(
            message="Submission completed successfully",
            data=result,
        )

ViewSet Organization

The ViewSet itself should remain thin.

A ViewSet may:

Authenticate users

Authorize users

Select the appropriate serializer

Validate request data through serializers

Retrieve objects through DRF mechanisms

Call services

Return responses using APIResponse

Define custom @action endpoints

A ViewSet must NOT:

Contain business logic

Perform complex calculations

Send emails directly

Call external APIs directly

Implement workflows

Perform complex database queries

Duplicate service-layer logic

Duplicate selector-layer logic

The architecture must remain:

Request
   ↓
Serializer
   ↓
ViewSet
   ↓
Service
   ↓
Selector
   ↓
Database

For custom actions:

Request
   ↓
ViewSet @action
   ↓
Serializer
   ↓
Service
   ↓
Selector
   ↓
Database

Example: Complete ViewSet

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from utils.response import APIResponse

from .serializers import (
    ApproveDocumentSerializer,
    BulkImportSerializer,
    DocumentSerializer,
)
from .services import DocumentService


class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return APIResponse.paginated(
                data=serializer.data,
                pagination={
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "page_size": self.paginator.page_size,
                    "current_page": self.paginator.page.number,
                    "total_pages": self.paginator.page.paginator.num_pages,
                },
                message="Documents retrieved successfully",
            )

        serializer = self.get_serializer(queryset, many=True)

        return APIResponse.success(
            message="Documents retrieved successfully",
            data=serializer.data,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = DocumentService.create(
            serializer.validated_data,
            request.user,
        )

        return APIResponse.created(
            message="Document created successfully",
            data=result,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return APIResponse.success(
            message="Document retrieved successfully",
            data=serializer.data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        result = DocumentService.update(
            instance,
            serializer.validated_data,
            request.user,
        )

        return APIResponse.success(
            message="Document updated successfully",
            data=result,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        DocumentService.delete(
            instance,
            request.user,
        )

        return APIResponse.success(
            message="Document deleted successfully",
            data=None,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        serializer = ApproveDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = self.get_object()

        result = DocumentService.approve(
            document=document,
            data=serializer.validated_data,
            user=request.user,
        )

        return APIResponse.success(
            message="Document approved successfully",
            data=result,
        )

    @action(detail=False, methods=["post"])
    def bulk_import(self, request):
        serializer = BulkImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = DocumentService.bulk_import(
            serializer.validated_data,
            request.user,
        )

        return APIResponse.success(
            message="Documents imported successfully",
            data=result,
        )

Mandatory Rule for AI Agents

When implementing any new API functionality, the AI agent MUST:

Determine the resource or business domain.

Create or identify the appropriate ViewSet.

Use ModelViewSet when normal CRUD is required.

Use ReadOnlyModelViewSet when only list/retrieve operations are required.

Use GenericViewSet with mixins when only a subset of CRUD operations is required.

Implement all non-CRUD operations using @action.

Never create APIView.

Never create GenericAPIView.

Never create DRF generic concrete views such as ListAPIView or CreateAPIView.

Never create Function Based Views.

Never use @api_view.

Register the ViewSet with a router whenever possible.

Keep business logic inside services.

Keep database access inside selectors.

Use serializers for request validation and response serialization.

Use APIResponse for every response.

Add pagination to list operations unless explicitly unnecessary.

Use DRF filtering, searching, and ordering instead of manually parsing query parameters.

Add appropriate permissions.

Add tests for the ViewSet and its actions.

Provide a proper commit message after every change, update, or feature.

Forbidden API Patterns

The following patterns are prohibited:

class MyAPIView(APIView):
    ...

class MyListView(ListAPIView):
    ...

class MyCreateView(CreateAPIView):
    ...

class MyGenericView(GenericAPIView):
    ...

@api_view(["POST"])
def create_document(request):
    ...

def create_document(request):
    ...

All of these must be replaced with a ViewSet implementation.

Correct Replacement Pattern

Instead of:

class ApproveDocumentAPIView(APIView):

    def post(self, request, pk):
        ...

use:

class DocumentViewSet(ModelViewSet):

    @action(
        detail=True,
        methods=["post"],
    )
    def approve(self, request, pk=None):
        ...

Instead of:

class DocumentListCreateView(ListCreateAPIView):
    ...

use:

class DocumentViewSet(ModelViewSet):
    ...

Instead of:

class DocumentDetailView(RetrieveUpdateDestroyAPIView):
    ...

use:

class DocumentViewSet(ModelViewSet):
    ...

Final View Rule

Every API endpoint MUST belong to a ViewSet.

CRUD endpoint
    ↓
ModelViewSet / GenericViewSet

Read-only endpoint
    ↓
ReadOnlyModelViewSet

Custom operation
    ↓
ViewSet @action

Everything else
    ↓
Design it as a ViewSet action

There is no APIView fallback.

There is no GenericAPIView fallback.

There is no Function Based View fallback.

ViewSet is mandatory.

Thin View Rule**

Views must remain thin.

Views may:

* Authenticate users
* Authorize users
* Validate requests
* Call services
* Return responses using APIResponse wrapper

Views must NOT:

* Contain business logic
* Perform calculations
* Send emails
* Call external APIs directly
* Implement workflows

Bad:

```python
class DocumentViewSet(ModelViewSet):

def create(self, request):
    \# 100 lines of business logic
    \# Manual error handling
    \# No universal response format

```

Good:

```python
class DocumentViewSet(ModelViewSet):

def create(self, request):
    serializer = self.get\_serializer(data=request.data)
    serializer.is\_valid(raise\_exception=True)
    result = DocumentService.create(serializer.validated\_data)
    return APIResponse.created(
        message="Document created successfully",
        data=result
    )

```

---

# Serializer Usage

Every endpoint must use serializers.

Never manually parse request data.

Bad:

```python
name = request.data.get("name")
```

Good:

```python
serializer = DocumentSerializer(
data=request.data
)
serializer.is_valid(
raise_exception=True
)
```

---

# Service Layer Rule

ViewSets, APIViews, and GenericViews must delegate business logic to services.

Example:

```python
class DocumentViewSet(ModelViewSet):

def perform\_create(self, serializer):
    result = DocumentService.create(
        serializer.validated\_data
    )
    return APIResponse.created(
        message="Document created successfully",
        data=result
    )

```

Never place business logic directly inside view methods.

---

# Custom Actions

For custom ViewSet operations use:

```python
@action(
detail=True,
methods=["post"]
)
def approve(self, request, pk=None):
document = self.get_object()
result = DocumentService.approve(document, request.user)
return APIResponse.success(
message="Document approved successfully",
data=result
)
```

or

```python
@action(
detail=False,
methods=["post"]
)
def bulk_import(self, request):
serializer = BulkImportSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
result = DocumentService.bulk_import(serializer.validated_data)
return APIResponse.success(
message=f"{len(result)} documents imported successfully",
data=result
)
```

Do not create separate APIViews if a ViewSet action is more appropriate.

---

# URL Standards

Prefer routers.

Example:

```python
router = DefaultRouter()

router.register(
"documents",
DocumentViewSet,
basename="documents"
)
```

Avoid manual URL mappings for CRUD endpoints.

---

# Pagination

All list endpoints must support pagination unless explicitly stated otherwise.

The AI agent must ask if pagination requirements are unclear.

**Paginated responses must use the paginated format:**

```python
return APIResponse.paginated(
data=serializer.data,
pagination={...},
message="Records retrieved successfully"
)
```

---

# Filtering

Use:

* django-filter
* DRF filter backends
* ordering filters
* search filters

Do not manually filter query parameters inside views.

---

# Settings Configuration

```python
# settings.py

REST_FRAMEWORK = {
'DEFAULT_RENDERER_CLASSES': [
'path.to.UniversalAPIJSONRenderer',  # Custom renderer
'rest_framework.renderers.BrowsableAPIRenderer',
],
'EXCEPTION_HANDLER': 'path.to.universal_exception_handler',
'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
'PAGE_SIZE': 10,
}
```

---

# Requirement Discovery Enforcement

Before creating any endpoint, the AI agent must ask:

1. Is this CRUD or workflow-based?
2. Should this be a ViewSet or APIView?
3. Who can access it?
4. Pagination required?
5. Search required?
6. Ordering required?
7. Filtering required?
8. Custom actions required?
9. Soft delete or hard delete?
10. Audit logging required?
11. **What success/error messages should be used?**
12. **What data structure should the response contain?**

The AI agent must not implement endpoints until these questions are answered.

---

# Django Admin Standards

## Mandatory Rule

**Every app that introduces a new business feature or manages persistent data must have a Django Admin interface.**

The AI agent must always create and maintain admin registrations for all models that require management through the Django Admin panel.

This is a mandatory requirement.

---

# Admin Registration

Every model that belongs to a feature must be registered in `admin.py`.

Example:

```python
from django.contrib import admin

from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
list_display = (
"id",
"title",
"status",
"created_at",
"updated_at",
)
search_fields = (
"title",
"status",
)
list_filter = (
"status",
"created_at",
)
ordering = ("-created_at",)
readonly_fields = (
"created_at",
"updated_at",
)
```

---

# Admin Requirements

Every `ModelAdmin` should include appropriate configuration whenever applicable:

* `list_display`
* `search_fields`
* `list_filter`
* `ordering`
* `readonly_fields`
* `list_per_page`
* `autocomplete_fields`
* `raw_id_fields`
* `date_hierarchy`
* `fieldsets` (for complex models)
* `inlines` (for related models)

The AI agent should configure these based on the model instead of using the default admin.

---

# Feature Completeness Rule

A feature is **not considered complete** until all of the following have been implemented:

* Models
* Migrations
* Serializers
* Views
* Services
* Selectors
* URLs
* Permissions (if required)
* Tests (if applicable)
* **Django Admin registration**

Missing Django Admin support means the feature is incomplete.

---

# Admin Coverage

Any app that stores or manages business data must expose its models in the Django Admin panel.

Examples include:

* Users
* Documents
* Orders
* Payments
* Transactions
* Bookkeeping
* Blogs
* AI Configurations
* Templates
* Categories
* Notifications
* Audit Logs
* Settings
* Reports

The only exceptions are:

* Abstract models
* Proxy models (unless explicitly required)
* Through models that should remain hidden
* Internal/system models that are not intended for administration

---

# AI Agent Enforcement

Whenever the AI agent:

* Creates a new model
* Adds a new app
* Introduces a new business feature
* Creates a persistent database table

it **must also**:

1. Register the model in `admin.py`.
2. Create a dedicated `ModelAdmin` class.
3. Configure `list_display`, `search_fields`, `list_filter`, and `ordering`.
4. Add `readonly_fields` for audit fields where appropriate.
5. Verify that the model is visible and manageable in the Django Admin panel.

---

# Final Rule

**Every feature that creates database-backed functionality must also provide a fully configured Django Admin interface.**

A pull request or implementation is **not complete** until the corresponding models can be viewed and managed through the Django Admin panel.

# Give a proper commit msg

1. after every change, update or adding feature agent should give proper commit msg

---

# Final Rule

Preferred Architecture:

Model
↓
Serializer
↓
ViewSet / GenericAPIView
↓
Service
↓
Selector
↓
Database

# deprecated apps
- w9_1099_chaser
- irs fire

# dont run the tests
- pls dont run the test

dont use the depricated apps

**All responses must use universal API response format.**

Function Based Views are prohibited.

ViewSets are preferred.

GenericAPIView is acceptable.

APIView is allowed only when justified.

**APIResponse wrapper is mandatory for all responses.**