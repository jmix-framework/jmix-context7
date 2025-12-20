<Path>Cookbook > Data in UI > Delayed data loading</Path>

This example shows how you can delay a costly data loading operation until the user has made the final selection of conditions. Try to select multiple rows in the left data grid displaying orders. The right data grid will be loaded in 2 sec after your last selection and will show all items of the selected orders with calculated total quantity, grouped by product name. The example uses a timer facet which is restarted on each selection change. The data loading is performed when the last timer goes off, that is in 2 sec after the last selection change. The left data grid is linked with a regular collection data container for the Order entity. It is loaded by the loader triggered in the BeforeShowEvent event handler. The right data grid is connected to a key-value container loaded with aggregated data. Its loader is triggered in the TimerActionEvent handler.

delayed-data-load.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="ordersDc" class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_base"/>
            <loader id="ordersDl" readOnly="true">
                <query>
                    <![CDATA[select o from uisamples_Order o order by o.date]]>
                </query>
            </loader>
        </collection>
        <keyValueCollection id="orderItemsDc">
            <loader id="orderItemsDl">
                <query>
                    <![CDATA[select o.product.name, SUM(o.quantity)
                    from OrderItem o
                    where o.order in :orders
                    group by o.product.name]]>
                </query>
            </loader>
            <properties>
                <property name="product" datatype="string"/>
                <property name="quantity" datatype="decimal"/>
            </properties>
        </keyValueCollection>
    </data>
    <facets>
        <timer id="timer" delay="2000"/>
    </facets>
    <layout>
        <hbox width="100%">
            <vbox padding="false">
                <h4 text="Orders"/>
                <dataGrid width="100%" id="ordersDataGrid" dataContainer="ordersDc" selectionMode="MULTI">
                    <columns>
                        <column property="date"/>
                        <column property="amount"/>
                        <column property="description"/>
                    </columns>
                </dataGrid>
            </vbox>
            <vbox padding="false">
                <h4 id="orderItemsHeader" text="Order Items">
                </h4>
                <dataGrid width="100%" id="orderItemsDataGrid" dataContainer="orderItemsDc">
                    <columns>
                        <column property="product" header="Product"/>
                        <column property="quantity" header="Total quantity"/>
                    </columns>
                </dataGrid>
            </vbox>
        </hbox>
    </layout>
</view>



DelayedDataLoad.java

package io.jmix.uisamples.view.flowui.cookbook.delayeddataload;


import com.vaadin.flow.component.html.H4;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.facet.Timer;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.model.KeyValueCollectionContainer;
import io.jmix.flowui.model.KeyValueCollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Order;

import java.util.Collections;
import java.util.Set;

@ViewController("delayed-data-load")
@ViewDescriptor("delayed-data-load.xml")
public class DelayedDataLoad extends StandardView {

    @ViewComponent
    private DataGrid<Order> ordersDataGrid;
    @ViewComponent
    private CollectionLoader<Order> ordersDl;
    @ViewComponent
    private KeyValueCollectionContainer orderItemsDc;
    @ViewComponent
    private KeyValueCollectionLoader orderItemsDl;
    @ViewComponent
    private H4 orderItemsHeader;
    @ViewComponent
    private Timer timer;

    @Subscribe
    public void onInit(final InitEvent event) {
        // Listen to selection changes
        ordersDataGrid.addSelectionListener(selectionEvent -> {
            refreshItems(selectionEvent.getAllSelectedItems());
        });
    }

    @Subscribe
    public void onBeforeShow(final BeforeShowEvent event) {
        // Load Orders on view opening
        ordersDl.load();
    }

    private void refreshItems(Set<Order> selectedOrders) {
        // When the selection changes, clear the OrderItems data grid and stop the timer
        orderItemsDc.setItems(Collections.emptyList());
        timer.stop();
        // If the selection is not empty, start the timer again
        // and set the parameter for loading OrderItems
        if (!selectedOrders.isEmpty()) {
            timer.start();
            orderItemsDl.setParameter("orders", selectedOrders);
            orderItemsHeader.setText("Waiting...");
        } else {
            orderItemsHeader.setText("Order Items");
        }
    }

    @Subscribe("timer")
    public void onTimerTimerAction(final Timer.TimerActionEvent event) {
        // Load OrderItems when the timer goes off using the latest parameter value
        orderItemsDl.load();
        orderItemsHeader.setText("Order Items");
    }
}



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




Product.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.CurrencyValue;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Table(name = "PRODUCT")
@Entity
@JmixEntity
public class Product {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", nullable = false)
    @InstanceName
    protected String name;

    @Column(name = "PRICE", nullable = false)
    @CurrencyValue(currency = "$")
    protected BigDecimal price;

    @JoinTable(name = "PRODUCT_PRODUCT_TAG_LINK",
            joinColumns = @JoinColumn(name = "PRODUCT_ID"),
            inverseJoinColumns = @JoinColumn(name = "PRODUCT_TAG_ID"))
    @ManyToMany
    private List<ProductTag> tags;

    public Product() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public List<ProductTag> getTags() {
        return tags;
    }

    public void setTags(List<ProductTag> tags) {
        this.tags = tags;
    }
}


