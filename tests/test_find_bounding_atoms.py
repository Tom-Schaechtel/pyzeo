def test_find_bounding_atoms():  
    """  
    Test the find_bounding_atoms method to identify atoms that bound channels.  
      
    This test follows the pattern established in other pyzeo tests:  
    1. Load a crystal structure (MgO)  
    2. Perform Voronoi decomposition with bvcells  
    3. Find channels in the network  
    4. For each channel, identify bounding atoms  
    5. Validate the results  
    """  
    from pyzeo.netstorage import AtomNetwork  
    from pyzeo.extension import find_channels  
    from pyzeo.extension import initializeMassTable, lookupRadius, lookupMass

    # initialize zeo++ default masses
    initializeMassTable()
    
    # rad_flag: whether to use atomic radii for Voronoi decomposition
    # by default atomic radii from zeo++ (from CCDC) are used
    atmnet = AtomNetwork.read_from_CIF("a_alsio2_pore.cif", rad_flag=True)
    
    # assign default zeo++ masses to atom objects of atmnet
    atmnet.loadMass()

    # Perform Voronoi decomposition with bvcells - modified method  
    vornet, edge_centers, fcs, bvcells = atmnet.perform_voronoi_decomposition(returnbvcells=True)  
 
    # Define probe radius for channel detection  
    probe_radius = 1.86 

    # Find channels using the new wrapper function  
    channels, access_info = find_channels(vornet, probe_radius)  

    print(f"Found {len(channels)} channels in the structure")  
    print(f"Accessibility info for {len(access_info)} nodes")

    # Test find_bounding_atoms for each channel  
    for i, channel in enumerate(channels):  
        # Call the find_bounding_atoms method  
        atom_ids = channel.find_bounding_atoms(atmnet, bvcells)  

        print(f"\nChannel {i}:")  
        print(f"  Number of bounding atoms: {len(atom_ids)}")  
        print(f"  Bounding atom IDs: {atom_ids}")  
          
        # Validate results  
        assert len(atom_ids) > 0, f"Channel {i} should have at least one bounding atom"  
        assert all(0 <= atom_id < atmnet.no_atoms for atom_id in atom_ids), \
            f"All atom IDs should be valid indices (0 to {atmnet.no_atoms-1})"  
          
        # Print atom details for the first few bounding atoms  
        for atom_id in atom_ids[:3]:  # Show first 3 atoms  
            atom = atmnet.atoms[atom_id]
            coords = atom.coords  

            print(f"    Atom {atom_id}: type={atom.type}, "  
                  f"coords=({coords[0]:.3f}, {coords[1]:.3f}, {coords[2]:.3f})")  
      
    print("\nTest completed successfully!")
  
