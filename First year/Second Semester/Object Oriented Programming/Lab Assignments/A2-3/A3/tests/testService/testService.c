#include <assert.h>
#include <string.h>
#include "testService.h"
#include "../../headers/service/service.h"

void TestService()
{
    TestCreateService();
    TestDestroyService();
    TestSaveBeforeOperation();
    TestAddEstate();
    TestDeleteEstate();
    TestUpdateEstate();
    TestGetAllEstates();
    TestGetAllEstatesContainingString();
    TestGetAllEstatesOfTypeHavingSurfaceGreaterThanAValue();
    TestSortEstatesBySurface();
    TestUndo();
    TestRedo();
}

void TestCreateService()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    assert(service->repository->estates->capacity == 2);
    assert(service->repository->estates->length == 0);
    assert(service->undoStack->stack->capacity == 2);
    assert(service->undoStack->stack->length == 0);
    assert(service->redoStack->stack->capacity == 2);
    assert(service->redoStack->stack->length == 0);
    DestroyService(service);
}

void TestDestroyService()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    DestroyService(service);
}

void TestSaveBeforeOperation()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    assert(service->undoStack->stack->length == 1);
    DestroyService(service);
}

void TestAddEstate()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    assert(AddEstate(service, estate) == 1);
    assert(AddEstate(service, estate) == 0);
    DestroyService(service);
}

void TestDeleteEstate()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    assert(DeleteEstate(service, "address") == 1);
    assert(DeleteEstate(service, "address") == 0);
    DestroyService(service);
}

void TestUpdateEstate()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    assert(UpdateEstate(service, "address", 1, 200, 20000) == 1);
    assert(UpdateEstate(service, "differentAddress", 1, 200, 20000) == 0);
    DestroyService(service);
}

void TestGetAllEstates()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    DynamicArray* estates = GetAllEstates(service);
    assert(estates->length == 1);
    DestroyService(service);
}

void TestGetAllEstatesContainingString()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    GetEstateAttribute GetAttribute = GetEstatePrice;
    DynamicArray* estates = GetAllEstatesContainingString(service, "address", GetAttribute);
    assert(estates->length == 1);
    DestroyService(service);
}

void TestGetAllEstatesOfTypeHavingSurfaceGreaterThanAValue()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    CompareEstate CompareFunction = CompareEstateSurfaceAscending;
    DynamicArray* estates = GetAllEstatesOfTypeHavingSurfaceGreaterThanAValue(service, 0, 0, CompareFunction);
    assert(estates->length == 1);
    DestroyService(service);
}

void TestSortEstatesBySurface()
{
    DynamicArray* estates = CreateDynamicArray(2, (DestroyFunction) DestroyEstate);
    Estate* estate1 = CreateEstate(0, "address1", 300, 10000);
    Estate* estate2 = CreateEstate(1, "address2", 200, 20000);
    CompareEstate CompareFunction = CompareEstateSurfaceAscending;
    AddElementToDynamicArray(estates, estate1);
    AddElementToDynamicArray(estates, estate2);
    SortEstatesBySurface(estates, CompareFunction);
    assert(strcmp(GetEstateAddress((Estate*) estates->elems[0]), "address2") == 0);
    assert(strcmp(GetEstateAddress((Estate*) estates->elems[1]), "address1") == 0);
}

void TestUndo()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    Undo(service);
    assert(service->repository->estates->length == 0);
    DestroyService(service);
}

void TestRedo()
{
    Service* service = CreateService(CreateRepository(),
                                     CreateStack(2, (DestroyFunction) DestroyRepository),
                                     CreateStack(2, (DestroyFunction) DestroyRepository));
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    AddEstate(service, estate);
    Undo(service);
    Redo(service);
    assert(service->repository->estates->length == 1);
    DestroyService(service);
}



