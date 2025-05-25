package com.selimhorri.app.e2e;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.selimhorri.app.dto.CartDto;
import com.selimhorri.app.dto.response.collection.DtoCollectionResponse;
import com.selimhorri.app.service.CartService;
import com.selimhorri.app.resource.CartResource;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(CartResource.class)
class CartResourceE2ETest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private CartService cartService;

    @Autowired
    private ObjectMapper objectMapper;

    private CartDto testCartDto;
    private List<CartDto> testCartList;

    @BeforeEach
    void setUp() {
        testCartDto = CartDto.builder()
                .cartId(1)
                .userId(100)
                .build();

        CartDto cart2 = CartDto.builder()
                .cartId(2)
                .userId(101)
                .build();

        testCartList = Arrays.asList(testCartDto, cart2);
    }

    @Test
    void testFindAll_ShouldReturnAllCarts() throws Exception {
        // Given
        when(cartService.findAll()).thenReturn(testCartList);

        // When & Then
        mockMvc.perform(get("/api/carts")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.collection").isArray())
                .andExpect(jsonPath("$.collection.length()").value(2))
                .andExpect(jsonPath("$.collection[0].cartId").value(1))
                .andExpect(jsonPath("$.collection[0].userId").value(100))
                .andExpect(jsonPath("$.collection[1].cartId").value(2))
                .andExpect(jsonPath("$.collection[1].userId").value(101));

        verify(cartService, times(1)).findAll();
    }

    @Test
    void testFindById_WithValidId_ShouldReturnCart() throws Exception {
        // Given
        when(cartService.findById(1)).thenReturn(testCartDto);

        // When & Then
        mockMvc.perform(get("/api/carts/1")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.cartId").value(1))
                .andExpect(jsonPath("$.userId").value(100));
        verify(cartService, times(1)).findById(1);
    }


    @Test
    void testSave_WithValidCart_ShouldCreateCart() throws Exception {
        // Given
        CartDto newCart = CartDto.builder()
                .userId(102)
                .build();

        CartDto savedCart = CartDto.builder()
                .cartId(3)
                .userId(102)
                .build();

        when(cartService.save(any(CartDto.class))).thenReturn(savedCart);

        // When & Then
        mockMvc.perform(post("/api/carts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(newCart)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.cartId").value(3))
                .andExpect(jsonPath("$.userId").value(102));

        verify(cartService, times(1)).save(any(CartDto.class));
    }

    @Test
    void testSave_WithNullCart_ShouldReturnBadRequest() throws Exception {
        // When & Then
        mockMvc.perform(post("/api/carts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("null"))
                .andExpect(status().isBadRequest());

        verify(cartService, never()).save(any(CartDto.class));
    }

    @Test
    void testUpdate_WithoutId_ShouldUpdateCart() throws Exception {
        // Given
        CartDto updatedCart = CartDto.builder()
                .cartId(1)
                .userId(100)
                .build();

        when(cartService.update(any(CartDto.class))).thenReturn(updatedCart);

        // When & Then
        mockMvc.perform(put("/api/carts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testCartDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.cartId").value(1));

        verify(cartService, times(1)).update(any(CartDto.class));
    }

    @Test
    void testUpdate_WithId_ShouldUpdateCartWithId() throws Exception {
        // Given
        CartDto updatedCart = CartDto.builder()
                .cartId(1)
                .userId(100)
                .build();

        when(cartService.update(eq(1), any(CartDto.class))).thenReturn(updatedCart);

        // When & Then
        mockMvc.perform(put("/api/carts/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testCartDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.cartId").value(1));

        verify(cartService, times(1)).update(eq(1), any(CartDto.class));
    }


    @Test
    void testUpdate_WithNullCart_ShouldReturnBadRequest() throws Exception {
        // When & Then
        mockMvc.perform(put("/api/carts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("null"))
                .andExpect(status().isBadRequest());

        verify(cartService, never()).update(any(CartDto.class));
    }

    @Test
    void testDeleteById_WithValidId_ShouldDeleteCart() throws Exception {
        // Given
        doNothing().when(cartService).deleteById(1);

        // When & Then
        mockMvc.perform(delete("/api/carts/1")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").value(true));

        verify(cartService, times(1)).deleteById(1);
    }


    // Integration Tests with Full Flow

    @Test
    void testSave_WithInvalidJson_ShouldReturnBadRequest() throws Exception {
        mockMvc.perform(post("/api/carts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{invalid json}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void testUpdate_WithMismatchedIds_ShouldUpdateWithProvidedId() throws Exception {
        CartDto cartWithDifferentId = CartDto.builder()
                .cartId(999) // Different from URL path
                .userId(100)
                .build();

        CartDto updatedCart = CartDto.builder()
                .cartId(1) // Should use ID from path
                .userId(100)
                .build();

        when(cartService.update(eq(1), any(CartDto.class))).thenReturn(updatedCart);

        mockMvc.perform(put("/api/carts/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(cartWithDifferentId)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.cartId").value(1));

        verify(cartService).update(eq(1), any(CartDto.class));
    }
}