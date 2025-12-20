<Path>Cookbook > Compositions > Order and uniqueness of items</Path>

This sample demonstrates how to implement ordering of composition items and ensure they have unique values within the root entity.

The composition consists of the `Order` and `OrderItem` entities. If you open an order for editing, you can see the data grid with items. The data grid has **#** column which shows the row number. You can move the item up and down with the corresponding buttons. When creating a new item or editing an existing one, the dropdown for selecting a product for the item contains only options that have not yet been added to the order.

Implementation details:

- [Order.java]({currentPath}?tab=Order.java)
    - `Order.items` attribute is annotated with `@Composition`.

- [OrderItem.java]({currentPath}?tab=OrderItem.java)
  - `OrderItem.rowNum` attribute stores the position of the item within the order.

- [OrderDetailView.java]({currentPath}?tab=OrderDetailView.java)
  - `itemsDataGridCreateActionInitializer()` handler sets initial value to `rowNum` by incrementing a maximum value among existing items.
  - `onItemsDcItemChange()` event handler enables and disables **Up** and **Down** buttons according to the position of the selected item.
  - `onUpButtonClick()` and `onDownButtonClick()` event listeners exchange `rowNum` between neighbour items and reorder table.
  - `itemsDataGridCreateActionViewConfigurer()` and `itemsDataGridEditActionViewConfigurer()` handlers pass a list of products already selected in the order items to `OrderItemDetailView`. This list is used to filter out already selected products from available options and thus ensure uniqueness of items in the order.

- [OrderItemDetailView.java]({currentPath}?tab=OrderItemDetailView.java)
  - `productFieldItemsFetchCallback()` handler loads available products according to the user input and the list of already added to the order products.


Order.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@Table(name = "ORDER")
@Entity(name = "uisamples_Order")
@JmixEntity
public class Order {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "CUSTOMER_ID")
    private Customer customer;

    @Temporal(TemporalType.DATE)
    @Column(name = "DATE_", nullable = false)
    @InstanceName
    private Date date;

    @Column(name = "AMOUNT")
    private BigDecimal amount;

    @Column(name = "DESCRIPTION")
    private String description;

    @OrderBy("rowNum")
    @Composition
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Date getDate() {
        return date;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public BigDecimal getAmount() {
        return amount;
    }
}




OrderItem.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.UUID;

@Table(name = "ORDER_ITEM")
@Entity
@JmixEntity
public class OrderItem {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "PRODUCT_ID")
    private Product product;

    @Column(name = "QUANTITY", precision = 19, scale = 3)
    private BigDecimal quantity;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ORDER_ID")
    private Order order;

    @Column(name = "ROW_NUM")
    private Integer rowNum;

    @InstanceName
    public String getInstanceName() {
        return product.getName() + " " + quantity;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setOrder(Order order) {
        this.order = order;
    }

    public Order getOrder() {
        return order;
    }

    public void setProduct(Product product) {
        this.product = product;
    }

    public Product getProduct() {
        return product;
    }

    public void setQuantity(BigDecimal quantity) {
        this.quantity = quantity;
    }

    public BigDecimal getQuantity() {
        return quantity;
    }

    public Integer getRowNum() {
        return rowNum;
    }

    public void setRowNum(Integer rowNum) {
        this.rowNum = rowNum;
    }
}




order-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://orderDetailView.title"
      focusComponent="form">
    <data>
        <instance id="orderDc"
                  class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_base">
                <property name="customer" fetchPlan="_base"/>
                <property name="items" fetchPlan="_base">
                    <property name="product" fetchPlan="_base"/>
                </property>
            </fetchPlan>
            <loader id="orderDl"/>
            <collection id="itemsDc" property="items"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="orderDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <entityPicker id="customerField" property="customer">
                <actions>
                    <action id="entityLookup" type="entity_lookup"/>
                    <action id="entityClear" type="entity_clear"/>
                </actions>
            </entityPicker>
            <datePicker id="dateField" property="date"/>
            <textField id="amountField" property="amount"/>
            <textField id="descriptionField" property="description"/>
        </formLayout>
        <h4 text="msg://io.jmix.uisamples.entity/Order.items"/>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button action="itemsDataGrid.createAction"/>
            <button action="itemsDataGrid.editAction"/>
            <button action="itemsDataGrid.removeAction"/>
            <button id="upButton" icon="vaadin:arrow-up" enabled="false" title="msg://upButton.title"/>
            <button id="downButton" icon="vaadin:arrow-down" enabled="false" title="msg://downButton.title"/>
        </hbox>
        <dataGrid id="itemsDataGrid" dataContainer="itemsDc" width="100%" minHeight="20em">
            <actions>
                <action id="createAction" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="order-item-detail-1"/>
                    </properties>
                </action>
                <action id="editAction" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="order-item-detail-1"/>
                    </properties>
                </action>
                <action id="removeAction" type="list_remove"/>
            </actions>
            <columns sortable="false">
                <column property="rowNum" width="10%"/>
                <column property="product" width="70%"/>
                <column property="quantity" width="20%"/>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




OrderDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition6;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.CollectionPropertyContainer;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Order;
import io.jmix.uisamples.entity.OrderItem;
import io.jmix.uisamples.entity.Product;

import java.util.Comparator;
import java.util.List;

@ViewController(id = "order-detail-1")
@ViewDescriptor(path = "order-detail-view.xml")
@EditedEntityContainer("orderDc")
public class OrderDetailView extends StandardDetailView<Order> {

    @ViewComponent
    private CollectionPropertyContainer<OrderItem> itemsDc;
    @ViewComponent
    private JmixButton upButton;
    @ViewComponent
    private JmixButton downButton;

    // Set initial sortValue
    @Install(to = "itemsDataGrid.createAction", subject = "initializer")
    private void itemsDataGridCreateActionInitializer(final OrderItem orderItem) {
        Integer maxValue = itemsDc.getItems().stream()
                .max(Comparator.comparing(OrderItem::getRowNum))
                .map(OrderItem::getRowNum)
                .orElse(0);
        orderItem.setRowNum(maxValue + 1);
    }

    // Enable and disable up/down buttons according to the position of selected item
    @Subscribe(id = "itemsDc", target = Target.DATA_CONTAINER)
    public void onItemsDcItemChange(final InstanceContainer.ItemChangeEvent<OrderItem> event) {
        upButton.setEnabled(false);
        downButton.setEnabled(false);

        OrderItem orderItem = event.getItem();
        if (orderItem != null) {
            int index = itemsDc.getItemIndex(orderItem);
            if (index > 0) {
                upButton.setEnabled(true);
            }
            if (index < itemsDc.getItems().size() - 1) {
                downButton.setEnabled(true);
            }
        }
    }

    // Exchange sortValue between neighbour items and reorder table after clicking Up
    @Subscribe(id = "upButton", subject = "clickListener")
    public void onUpButtonClick(final ClickEvent<JmixButton> event) {
        OrderItem currentItem = itemsDc.getItemOrNull();
        if (currentItem != null) {
            currentItem.setRowNum(currentItem.getRowNum() - 1);

            OrderItem prevItem = itemsDc.getItems().get(itemsDc.getItemIndex(currentItem) - 1);
            prevItem.setRowNum(prevItem.getRowNum() + 1);

            itemsDc.getDisconnectedItems().sort(Comparator.comparing(OrderItem::getRowNum));
        }
    }

    // Exchange sortValue between neighbour items and reorder table after clicking Down
    @Subscribe(id = "downButton", subject = "clickListener")
    public void onDownButtonClick(final ClickEvent<JmixButton> event) {
        OrderItem currentItem = itemsDc.getItemOrNull();
        if (currentItem != null) {
            currentItem.setRowNum(currentItem.getRowNum() + 1);

            OrderItem nextItem = itemsDc.getItems().get(itemsDc.getItemIndex(currentItem) + 1);
            nextItem.setRowNum(nextItem.getRowNum() - 1);

            itemsDc.getDisconnectedItems().sort(Comparator.comparing(OrderItem::getRowNum));
        }
    }

    // Pass already added products to opened OrderItemDetailView to filter them out from options
    @Install(to = "itemsDataGrid.createAction", subject = "viewConfigurer")
    private void itemsDataGridCreateActionViewConfigurer(final OrderItemDetailView orderItemDetailView) {
        List<Product> addedProducts = itemsDc.getItems().stream()
                .map(OrderItem::getProduct)
                .toList();
        orderItemDetailView.setAddedProducts(addedProducts);
    }

    // Pass already added products to opened OrderItemDetailView to filter them out from options.
    // When editing an item, the product selected in this item should also be available,
    // which is achieved by the `filter()` operation.
    @Install(to = "itemsDataGrid.editAction", subject = "viewConfigurer")
    private void itemsDataGridEditActionViewConfigurer(final OrderItemDetailView orderItemDetailView) {
        List<Product> addedProducts = itemsDc.getItems().stream()
                .filter(orderItem -> orderItem != itemsDc.getItem())
                .map(OrderItem::getProduct)
                .toList();
        orderItemDetailView.setAddedProducts(addedProducts);
    }
}




order-item-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://orderItemDetailView.title"
      focusComponent="form">
    <data>
        <instance id="orderItemDc"
                  class="io.jmix.uisamples.entity.OrderItem">
            <fetchPlan extends="_base">
                <property name="product" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="orderItemDl"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="orderItemDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <entityComboBox id="productField" property="product">
                <actions>
                    <action id="entityClear" type="entity_clear"/>
                </actions>
            </entityComboBox>
            <textField id="quantityField" property="quantity"/>
        </formLayout>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




OrderItemDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition6;

import com.vaadin.flow.data.provider.Query;
import io.jmix.core.DataManager;
import io.jmix.core.Sort;
import io.jmix.core.querycondition.LogicalCondition;
import io.jmix.core.querycondition.PropertyCondition;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.OrderItem;
import io.jmix.uisamples.entity.Product;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.UUID;
import java.util.stream.Stream;

@ViewController(id = "order-item-detail-1")
@ViewDescriptor(path = "order-item-detail-view.xml")
@EditedEntityContainer("orderItemDc")
public class OrderItemDetailView extends StandardDetailView<OrderItem> {

    @Autowired
    private DataManager dataManager;

    private List<UUID> addedProductIds;

    public void setAddedProducts(List<Product> addedProducts) {
        this.addedProductIds = addedProducts.stream().map(Product::getId).toList();
    }

    @Install(to = "productField", subject = "itemsFetchCallback")
    private Stream<Product> productFieldItemsFetchCallback(final Query<Product, String> query) {
        String param = query.getFilter().orElse("");
        return dataManager.load(Product.class)
                .condition(LogicalCondition.and(
                        PropertyCondition.notInList("id", addedProductIds),
                        PropertyCondition.contains("name", param)
                ))
                .sort(Sort.by("name"))
                .firstResult(query.getOffset())
                .maxResults(query.getLimit())
                .list()
                .stream();
    }
}


