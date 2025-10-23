def main():
    import elysia
    from elysia import configure, preprocess
    import os
    
    try:
        wcd_url = os.getenv("WCD_URL", "your-weaviate-url-here") 
        wcd_key = os.getenv("WCD_API_KEY", "your-weaviate-api-key-here")
        
        
        print("Configuring Elysia...")
        configure(
            wcd_url=wcd_url,
            wcd_api_key=wcd_key
        )
        print("✓ Configuration complete!")
        
        # Preprocess the Ecommerce collection
        print("Preprocessing Ecommerce collection...")
        preprocess("Ecommerce")
        print("✓ Collection preprocessing complete!")
        
        # Create and use the Tree
        print("Creating Tree and querying...")
        tree = elysia.Tree()
        response, objects = tree(
            "What are the 10 most expensive items in the Ecommerce collection?"
        )
        
        print("\n" + "="*50)
        print("QUERY RESULTS:")
        print("="*50)
        print("Response:", response)
        print(f"Retrieved objects: {len(objects) if objects else 0}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your API keys are correct")
        print("2. Ensure your Weaviate cluster is accessible")
        print("3. Verify the 'Ecommerce' collection exists in your Weaviate cluster")
        print("4. Check that you have the required permissions")


if __name__ == "__main__":
    main()
