<Path>Components > CheckboxGroup > Data-aware CheckboxGroup</Path>

The CheckboxGroup component can take a list of items from a data container. For this purpose, the itemsContainer attribute is used.

checkbox-group-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="productsDc"
                    class="io.jmix.uisamples.entity.Product"
                    fetchPlan="_local">
            <loader id="productsLoader">
                <query>
                    <![CDATA[select e from Product e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <checkboxGroup id="checkboxGroup"
                       itemsContainer="productsDc"
                       themeNames="vertical"/>
    </layout>
</view>




CheckboxGroupDataawareSample.java

package io.jmix.uisamples.view.flowui.components.checkboxgroup.dataaware;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("checkbox-group-dataaware")
@ViewDescriptor("checkbox-group-dataaware.xml")
public class CheckboxGroupDataawareSample extends StandardView {
}




Product.java

package io.jmix.uisamples.entity;

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


