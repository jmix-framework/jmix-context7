<Path>Cookbook > Compositions > Informing about changes in composition</Path>

This sample demonstrates how to inform users about changes in the whole composition including nested dialog windows.

The composition consists of the `Order` and `OrderItem` entities. When you open an order to edit, you can see the **No changes detected** message at the top of the order detail view. The message will change to **There are unsaved changes!** if you change any fields in this view, as well as if you create or remove an order item or edit an order item in its detail view.    

Implementation details:

- [Order.java]({currentPath}?tab=Order.java)
    - `Order.items` attribute is annotated with `@Composition`.

- [order-detail-view.xml]({currentPath}?tab=order-detail-view.xml)
  - The `<div id="infoPanel">` element defines the initial state of the info panel.

- [OrderDetailView.java]({currentPath}?tab=OrderDetailView.java)
  - `updateInfoPanel()` method updates the info panel when changes are detected.
  - `onChange()` event listener calls `updateInfoPanel()` when the `DataContext` of this view detects changes in its entities. It happens, for example, when the user modifies the `date` attribute or the `items` collection. However, this listener does not react to changes made in the separate `OrderItemDetailView`. This is why `updateInfoPanel()` should also be called from the `OrderItemDetailView` itself.
  - `itemsDataGridEditActionViewConfigurer()` handler passes the reference to `updateInfoPanel()` to `OrderItemDetailView`.
  
- [OrderItemDetailView.java]({currentPath}?tab=OrderItemDetailView.java)
  - `onPostSave()` event listener calls `updateInfoPanel()` after the user clicks **OK** and the changes are saved by the `DataContext` of this view. We cannot use `onChange()` event listener here because changes in this view can be canceled by the user. 


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
        <div id="infoPanel" themeNames="badge success" text="msg://infoPanel.text.noChanges" height="2em" alignSelf="CENTER"/>
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
        <hbox id="buttonsPanel" width="100%" wrap="true">
            <button action="itemsDataGrid.createAction"/>
            <button action="itemsDataGrid.editAction"/>
            <button action="itemsDataGrid.removeAction"/>
        </hbox>
        <dataGrid id="itemsDataGrid" dataContainer="itemsDc" width="100%" minHeight="10em">
            <actions>
                <action id="createAction" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="order-item-detail-2"/>
                    </properties>
                </action>
                <action id="editAction" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="order-item-detail-2"/>
                    </properties>
                </action>
                <action id="removeAction" type="list_remove"/>
            </actions>
            <columns sortable="false">
                <column property="product"/>
                <column property="quantity"/>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




OrderDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition7;

import com.vaadin.flow.component.html.Div;
import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Order;

@ViewController(id = "order-detail-2")
@ViewDescriptor(path = "order-detail-view.xml")
@EditedEntityContainer("orderDc")
public class OrderDetailView extends StandardDetailView<Order> {

    @ViewComponent
    private Div infoPanel;
    @ViewComponent
    private MessageBundle messageBundle;

    @Subscribe(target = Target.DATA_CONTEXT)
    public void onChange(final DataContext.ChangeEvent event) {
        updateInfoPanel();
    }

    @Install(to = "itemsDataGrid.editAction", subject = "viewConfigurer")
    private void itemsDataGridEditActionViewConfigurer(final OrderItemDetailView orderItemDetailView) {
        orderItemDetailView.setChangeEventListener(this::updateInfoPanel);
    }

    private void updateInfoPanel() {
        infoPanel.setText(messageBundle.getMessage("infoPanel.text.unsavedChanges"));
        infoPanel.getElement().getThemeList().remove("success");
        infoPanel.getElement().getThemeList().add("error");
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
                <itemsQuery class="io.jmix.uisamples.entity.Product" escapeValueForLike="true"
                            searchStringFormat="(?i)%${inputString}%">
                    <fetchPlan extends="_base"/>
                    <query>
                        <![CDATA[select e from Product e where e.name like :searchString escape '\' order by e.name]]>
                    </query>
                </itemsQuery>
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

package io.jmix.uisamples.view.flowui.cookbook.composition7;

import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.OrderItem;

@ViewController(id = "order-item-detail-2")
@ViewDescriptor(path = "order-item-detail-view.xml")
@EditedEntityContainer("orderItemDc")
public class OrderItemDetailView extends StandardDetailView<OrderItem> {

    private Runnable updateInfoPanel;

    public void setChangeEventListener(Runnable updateInfoPanel) {
        this.updateInfoPanel = updateInfoPanel;
    }

    @Subscribe(target = Target.DATA_CONTEXT)
    public void onPostSave(final DataContext.PostSaveEvent event) {
        if (!event.getSavedInstances().isEmpty() && updateInfoPanel != null)
            updateInfoPanel.run();
    }
}


